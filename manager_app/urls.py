from django.urls import path

from manager_app.views import index


app_name = "manager_app"
urlpatterns = [
    path("", index, name="index"),
]