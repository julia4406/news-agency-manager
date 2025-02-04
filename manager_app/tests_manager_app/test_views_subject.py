from http.client import responses

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from manager_app.models import Editor, Subject

SUBJECT_LIST_URL = reverse("manager_app:subject-list")
# PUBLICATION_DETAIL_URL = reverse("manager_app:publication-detail")


class SubjectViewTests(TestCase):
    fixtures = [
        "test_data.json",
    ]

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="123_teSt",
            first_name="Test",
            last_name="Bytest",
            email="test123@test.te",
            experience=5,
        )
        self.client.force_login(self.user)

    def test_subject_user_has_to_be_logged(self):
        self.client.logout()
        response = self.client.get(SUBJECT_LIST_URL)
        self.assertEqual(response.status_code, 302)

    def test_subject_list_response_with_correct_template(self):
        response = self.client.get(SUBJECT_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "manager_app/subject_list.html"
        )

    def test_subject_list_ordered_by_name(self):
        response = self.client.get(SUBJECT_LIST_URL)
        subject_context = response.context["subjects"]

        subjects = Subject.objects.all().order_by("name")

        self.assertEqual(
            list(subject_context),
            list(subjects[:len(subject_context)])
        )