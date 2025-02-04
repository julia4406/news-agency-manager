from http.client import responses
from idlelib.rpc import response_queue

from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.test import TestCase
from django.urls import reverse

from manager_app.forms import EditorForm
from manager_app.models import Editor, Publication, Subject

EDITOR_LIST_URL = reverse("manager_app:editor-list")
# PUBLICATION_DETAIL_URL = reverse("")


class EditorViewTests(TestCase):
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

    def test_editor_user_has_to_be_logged(self):
        self.client.logout()
        response = self.client.get(EDITOR_LIST_URL)
        self.assertEqual(response.status_code, 302)

    def test_editor_list_response_with_correct_template(self):
        response = self.client.get(EDITOR_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "manager_app/editor-list.html"
        )

    def test_editor_list_annotated_and_ordered_by_last_name(self):
        response = self.client.get(EDITOR_LIST_URL)
        editor_context = response.context["editor_list"]

        editors = Editor.objects.annotate(
            overdues=Count(
                "publications",
                filter=Q(publications__status="Overdue")
            )).order_by("last_name")

        self.assertEqual(
            list(editor_context),
            list(editors[:len(editor_context)])
        )

    def test_create_editor(self):
        # subject = Subject.objects.create(name="Test Subject")
        # editor = get_user_model().objects.create(username="editor_user")

        response = self.client.post(
            reverse(
                "manager_app:editor-create"
            ),
            {
                "password": "pbTest_4=",
                "username": "test123",
                "experience": 4,
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Editor.objects.get(username="test123").experience,
            4
        )