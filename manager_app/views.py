from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from manager_app.models import Editor, Publication, Subject


def index(request: HttpRequest) -> HttpResponse:
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
        "manager_app/index.html",
        context=context
    )