from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Subject(models.Model):
    name = models.CharField(max_length=50)


class Editor(AbstractUser):
    experience = models.PositiveIntegerField()

    def __str__(self):
        return (f"Editor {self.username}: {self.first_name} {self.last_name}, "
                f"{self.experience} years of experience")

    def get_absolute_url(self):
        return reverse("manager_app:editor-detail", kwargs={"pk": self.pk})


class Publication(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    publication_date  = models.DateField()
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="publications"
    )
    executives = models.ManyToManyField(
        Editor,through="PublicationEditor", related_name="publications"
    )

    def __str__(self):
        return f"{self.title}, deadline {self.publication_date}, subject: {self.subject.name}"

    def get_absolute_url(self):
        return reverse("manager_app:publication-detail", kwargs={"pk": self.pk})


class PublicationEditor(models.Model):
    editor = models.ForeignKey(Editor, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    assigned_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ("publication", "editor")

    def __str__(self):
        return f"{self.editor.username} assigned to {self.publication.title} on {self.assigned_at}"
