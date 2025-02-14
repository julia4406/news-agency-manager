from datetime import timedelta

from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from manager_app.models import Editor, Publication, Subject
from manager_app.choices import TaskStatuses
from manager_app.forms import (
    LoginForm,
    PublicationForm,
    EditorForm,
    SubjectForm,
    EditorUpdateForm,
    SearchEditorsInPublicationsForm,
)


def index(request):
    num_editors = Editor.objects.count()
    num_publications = Publication.objects.count()
    num_subjects = Subject.objects.count()

    context = {
        "num_editors": num_editors,
        "num_publications": num_publications,
        "num_subjects": num_subjects,
    }
    return render(request, "pages/index.html", context=context)


class PublicationListView(LoginRequiredMixin, ListView):
    model = Publication
    paginate_by = 5
    template_name = "manager_app/publication-list.html"
    context_object_name = "publication_list"

    def get_queryset(self):
        queryset = (
            Publication.objects.select_related("subject")
            .prefetch_related("executives")
            .order_by("publication_date", "status")
        )
        today = timezone.now().date()

        (
            queryset.filter(publication_date__lte=today)
            .exclude(status=TaskStatuses.DONE)
            .update(status=TaskStatuses.OVERDUE)
        )

        form = SearchEditorsInPublicationsForm(self.request.GET)

        if form.is_valid() and form.cleaned_data["query"]:
            return queryset.filter(
                executives__last_name__icontains=form.cleaned_data["query"]
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        two_day_gap = today + timedelta(days=2)
        context["two_day_gap"] = two_day_gap

        context["search"] = SearchEditorsInPublicationsForm()

        referer_url = self.request.META.get("HTTP_REFERER", "/")
        context["previous"] = referer_url

        return context


class PublicationDetailView(LoginRequiredMixin, DetailView):
    model = Publication
    queryset = Publication.objects.select_related("subject").prefetch_related(
        "executives"
    )
    template_name = "manager_app/publication-detail.html"


class PublicationCreateView(LoginRequiredMixin, CreateView):
    model = Publication
    form_class = PublicationForm
    success_url = reverse_lazy("manager_app:publication-list")


class PublicationUpdateView(LoginRequiredMixin, UpdateView):
    model = Publication
    form_class = PublicationForm
    template_name = "manager_app/publication_form.html"
    context_object_name = "publication"
    success_url = reverse_lazy("manager_app:publication-list")


def update_status_of_publication(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    today = timezone.now().date()

    if publication.status == TaskStatuses.ASSIGNED:
        publication.status = TaskStatuses.DONE

    elif publication.status == TaskStatuses.DONE:
        publication.status = TaskStatuses.ASSIGNED

    elif (
        publication.status == TaskStatuses.OVERDUE
        and publication.publication_date > today
    ):
        publication.status = TaskStatuses.ASSIGNED

    publication.save()
    referer_url = request.META.get("HTTP_REFERER", "/")

    return redirect(referer_url)


class PublicationDeleteView(LoginRequiredMixin, DeleteView):
    model = Publication
    success_url = reverse_lazy("manager_app:publication-list")


class EditorListView(LoginRequiredMixin, ListView):
    model = Editor
    paginate_by = 5
    template_name = "manager_app/editor-list.html"
    context_object_name = "editor_list"

    def get_queryset(self):

        queryset = Editor.objects.annotate(
            overdues=Count(
                "publications",
                filter=Q(publications__status="Overdue")
            )
        ).order_by("last_name")
        return queryset


class EditorDetailView(LoginRequiredMixin, DetailView):
    model = Editor
    template_name = "manager_app/editor-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        editor = self.get_object()
        context["publications"] = editor.publications.all()

        return context


class EditorCreateView(LoginRequiredMixin, CreateView):
    model = Editor
    form_class = EditorForm
    success_url = reverse_lazy("manager_app:editor-list")


class EditorUpdateView(LoginRequiredMixin, UpdateView):
    model = Editor
    form_class = EditorUpdateForm
    template_name = "manager_app/editor_form.html"
    context_object_name = "editor"
    success_url = reverse_lazy("manager_app:editor-list")


class EditorDeleteView(LoginRequiredMixin, DeleteView):
    model = Editor
    success_url = reverse_lazy("manager_app:editor-list")


class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    queryset = Subject.objects.all().order_by("name")
    paginate_by = 5
    context_object_name = "subjects"
    template_name = "manager_app/subject_list.html"


class SubjectCreateView(LoginRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = "manager_app/subject_form.html"
    success_url = reverse_lazy("manager_app:subject-list")


class SubjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = "manager_app/subject_form.html"
    success_url = reverse_lazy("manager_app:subject-list")


class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Subject
    success_url = reverse_lazy("manager_app:subject-list")


class SubjectRelatedPublicationsListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = "manager_app/subject-publications.html"
    context_object_name = "publications"

    def get_queryset(self):
        return Publication.objects.filter(subject_id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["subject"] = Subject.objects.get(pk=self.kwargs["pk"])
        return context


class UserLoginView(auth_views.LoginView):
    template_name = "accounts/sign-in.html"
    form_class = LoginForm
    success_url = "pages/index.html"

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")

        if not remember_me:
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(1209600)  # 14 days

        return super().form_valid(form)


def user_logout_view(request):
    logout(request)
    return redirect("/accounts/login/")


def contact_us(request):
    return render(request, "pages/contact-us.html")


def about_us(request):
    return render(request, "pages/about-us.html")


def author(request):
    return render(request, "pages/author.html")


def page_header(request):
    return render(request, "sections/page-sections/hero-sections.html")


def under_construction(request):
    return render(request, "under_construction.html")
