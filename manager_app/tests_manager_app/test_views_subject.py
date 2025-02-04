from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from manager_app.models import Subject, Publication


SUBJECT_LIST_URL = reverse("manager_app:subject-list")


class SubjectViewTests(TestCase):
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

    def test_create_subject(self):
        response = self.client.post(
            reverse(
                "manager_app:subject-create"
            ),
            {"name": "test_subject"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Subject.objects.get(name="test_subject").name,
            "test_subject"
        )

    def test_update_subject(self):
        subject = Subject.objects.create(
            name="test_subject"
        )
        form_data = {"name": "new_test_subject"}
        response = self.client.post(
            reverse(
                "manager_app:subject-update",
                kwargs={"pk": subject.id}
            ),
            data=form_data,
        )
        subject.refresh_from_db()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(subject.name, "new_test_subject")

    def test_delete_subject(self):
        subject = Subject.objects.create(
            name="test_subject"
        )

        response = self.client.post(
            reverse(
                "manager_app:subject-delete",
                kwargs={"pk": subject.id}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Subject.objects.filter(id=subject.id).exists())

    def test_subject_has_list_of_related_publications(self):
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
            reverse("manager_app:subject-related", kwargs={"pk": subject.id})
        )

        self.assertEqual(response.status_code, 200)

        publications = response.context["publications"]
        self.assertIn(pub1, publications)
        self.assertIn(pub2, publications)
