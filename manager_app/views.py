from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from manager_app.forms import (
    LoginForm,
    # RegistrationForm,
    # UserPasswordResetForm,
    # UserSetPasswordForm,
    # UserPasswordChangeForm,
    PublicationForm,
)
from django.contrib.auth import logout

from django.contrib.auth import views as auth_views

#----------------mine--------------------
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from manager_app.models import Editor, Publication, Subject



def index(request):
    num_editors = Editor.objects.count()
    num_publications = Publication.objects.count()
    num_subjects = Subject.objects.count()
    num_visits = request.session.get("num_visits", 0)
    num_visits += 1
    request.session["num_visits"] = num_visits
    context = {
        "num_editors": num_editors,
        "num_publications": num_publications,
        "num_subjects": num_subjects,
        "num_visits": num_visits,
    }
    return render(
        request,
        "pages/index.html",
        context=context
    )


class PublicationListView(LoginRequiredMixin, ListView):
    model = Publication
    paginate_by = 5
    template_name = "manager_app/publication-list.html"
    context_object_name = "publication_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        two_day_gap = today + timedelta(days=2)
        context["two_day_gap"] = two_day_gap
        return context


class PublicationDetailView(LoginRequiredMixin, DetailView):
    model = Publication
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


class PublicationDeleteView(LoginRequiredMixin, DeleteView):
    model = Publication
    success_url = reverse_lazy("manager_app:publication-list")



def under_construction(request):
    return render(request, "under_construction.html")

#------------TEMPLATE VIEWS Material Kit----------------------
# Authentication
# def registration(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             print('Account created successfully!')
#             return redirect('/accounts/login/')
#         else:
#             print("Registration failed!")
#     else:
#         form = RegistrationForm()
#
#     context = {'form': form}
#     return render(request, 'accounts/sign-up.html', context)
#
#
class UserLoginView(auth_views.LoginView):
    template_name = "accounts/sign-in.html"
    form_class = LoginForm
    success_url = "pages/index.html"

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(1209600)  # 14 days

        return super().form_valid(form)

#
# class UserPasswordResetView(auth_views.PasswordResetView):
#     template_name = 'accounts/password_reset.html'
#     form_class = UserPasswordResetForm
#
#
# class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
#     template_name = 'accounts/password_reset_confirm.html'
#     form_class = UserSetPasswordForm
#
#
# class UserPasswordChangeView(auth_views.PasswordChangeView):
#     template_name = 'accounts/password_change.html'
#     form_class = UserPasswordChangeForm
#
#
def user_logout_view(request):
    logout(request)
    return redirect("/accounts/login/")


# Pages

def contact_us(request):
    return render(request, "pages/contact-us.html")


def about_us(request):
    return render(request, "pages/about-us.html")


def author(request):
    return render(request, "pages/author.html")


# # Sections
# def presentation(request):
#     return render(request, 'sections/presentation.html')
#
#
def page_header(request):
    return render(request, "sections/page-sections/hero-sections.html")

#
# def features(request):
#     return render(request, 'sections/page-sections/features.html')
#
#
# def navbars(request):
#     return render(request, 'sections/navigation/navbars.html')
#
#
# def nav_tabs(request):
#     return render(request, 'sections/navigation/nav-tabs.html')
#
#
# def pagination(request):
#     return render(request, 'sections/navigation/pagination.html')
#
#
# def forms(request):
#     return render(request, 'sections/input-areas/forms.html')
#
#
# def inputs(request):
#     return render(request, 'sections/input-areas/inputs.html')
#
#
# def avatars(request):
#     return render(request, 'sections/elements/avatars.html')
#
#
# def badges(request):
#     return render(request, 'sections/elements/badges.html')
#
#
# def breadcrumbs(request):
#     return render(request, 'sections/elements/breadcrumbs.html')
#
#
# def buttons(request):
#     return render(request, 'sections/elements/buttons.html')
#
#
# def dropdowns(request):
#     return render(request, 'sections/elements/dropdowns.html')
#
#
# def progress_bars(request):
#     return render(request, 'sections/elements/progress-bars.html')
#
#
# def toggles(request):
#     return render(request, 'sections/elements/toggles.html')
#
#
# def typography(request):
#     return render(request, 'sections/elements/typography.html')
#
#
# def alerts(request):
#     return render(request, 'sections/attention-catchers/alerts.html')
#
#
# def modals(request):
#     return render(request, 'sections/attention-catchers/modals.html')
#
#
# def tooltips(request):
#     return render(request, 'sections/attention-catchers/tooltips-popovers.html')