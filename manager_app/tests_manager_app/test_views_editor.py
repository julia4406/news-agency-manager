from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.test import TestCase
from django.urls import reverse

from manager_app.models import Editor, Publication, Subject


EDITOR_LIST_URL = reverse("manager_app:editor-list")


class EditorViewTests(TestCase):
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

    def test_editor_detail_view_gets_publications(self):
        subject = Subject.objects.create(
            name="test_subject"
        )

        pub1 = Publication.objects.create(
            title="test_publication1",
            content="test bla-bla",
            publication_date="2025-09-04",
            subject=subject,
        )
        pub1.executives.set([self.user])

        pub2 = Publication.objects.create(
            title="test_publication2",
            content="test ololo",
            publication_date="2026-02-04",
            subject=subject,
        )
        pub2.executives.set([self.user])

        response = self.client.get(
            reverse(
                "manager_app:editor-detail",
                kwargs={"pk": self.user.id}
            )
        )

        self.assertEqual(response.status_code, 200)

        publications = response.context["publications"]
        self.assertIn(pub1, publications)
        self.assertIn(pub2, publications)

    def test_create_editor(self):
        form_data = {
            "username": "not_admin_user",
            "first_name": "Not Admin",
            "last_name": "User",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
            "email": "test@te.st",
            "experience": 3,
        }
        response = self.client.post(
            reverse("manager_app:editor-create"), data=form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Editor.objects.get(username="not_admin_user").username,
            "not_admin_user"
        )

    def test_update_editor(self):
        form_data = {
            "username": "not_admin_user",
            "first_name": "Not Admin",
            "last_name": "User",
            "password": "1qazcde3",
            "email": "test@te.st",
            "experience": 3,
        }
        new_data = {
            "username": "not_admin_user",
            "first_name": "Paul",
            "last_name": "Tester",
            "password": "1qazcde3",
            "email": "test@te.st",
            "experience": 1,
        }

        editor = get_user_model().objects.create_user(**form_data)
        response = self.client.post(
            reverse("manager_app:editor-update", kwargs={"pk": editor.id}),
            data=new_data
        )
        editor.refresh_from_db()
        print(Editor.objects.all().values())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(editor.first_name, "Paul")

    def test_delete_editor(self):
        editor = get_user_model().objects.create_user(
            username="not_admin.user",
            first_name="Not Admin",
            last_name="User",
            password="1qazcde3",
            email="test@te.st",
            experience=3,
        )
        response = self.client.post(
            reverse(
                "manager_app:editor-delete",
                kwargs={"pk": editor.id}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            get_user_model().objects.filter(id=editor.id).exists()
        )
