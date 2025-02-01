from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from manager_app.models import Editor, Publication, Subject


admin.site.unregister(Group)


@admin.register(Editor)
class EditorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("experience",)
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("experience",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": (
            "first_name",
            "last_name",
            "experience",
        )}),
    )
    search_fields = ["username", "first_name", "last_name"]
    list_filter = ["experience"]


@admin.register(Publication)
class CarAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_filter = ["executives"]


admin.site.register(Subject)
