from http.client import responses

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from manager_app.models import Editor, Publication, Subject

PUBLICATION_LIST_URL = reverse("manager_app:publication-list")


class PublicationViewTests(TestCase):
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

    def test_publication_user_has_to_be_logged(self):
        self.client.logout()
        response = self.client.get(PUBLICATION_LIST_URL)
        self.assertEqual(response.status_code, 302)

    def test_publication_list_response_with_correct_template(self):
        response = self.client.get(PUBLICATION_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "manager_app/publication-list.html"
        )

    def test_publication_list_ordered_by_publication_data(self):
        response = self.client.get(PUBLICATION_LIST_URL)
        publication_context = response.context["publication_list"]

        publications = (Publication.objects.all()
                        .order_by("publication_date", "status"))

        self.assertEqual(
            list(publication_context),
            list(publications[:len(publication_context)])
        )

    def test_create_publication(self):
        subject = Subject.objects.create(name="Test Subject")
        editor = get_user_model().objects.create(username="editor_user")

        response = self.client.post(
            reverse(
                "manager_app:publication-create"
            ),
            {
                "title": "test_publication",
                "content": "test content content content content",
                "publication_date": "2025-02-04",
                "subject": subject.id,
                "status": "Overdue",
                "executives": [editor.id],
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Publication.objects.get(title="test_publication").title,
            "test_publication"
        )

    def test_update_publication(self):
        subject = Subject.objects.create(name="Test Subject")
        editor = get_user_model().objects.create(username="editor_user")
        publication = Publication.objects.create(
            title="test_publication",
            content="test content content content content",
            publication_date="2025-02-04",
            subject=subject,
            status="Overdue",
        )
        publication.executives.set([editor])
        form_data = {
                "title": "new_test_publication",
                "content": "new test content",
            }
        response = self.client.post(
            reverse(
                "manager_app:publication-update",
                kwargs={"pk": publication.id}
            ),
            data=form_data,
        )
        publication.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            publication.title,
            "new_test_publication"
        )

    # def test_delete_car(self):
    #     car = Car.objects.create(
    #         model="Continental",
    #         manufacturer=self.manufacturer,
    #     )
    #     response = self.client.post(
    #         reverse("taxi:car-delete", kwargs={"pk": car.id})
    #     )
    #     self.assertEqual(response.status_code, 302)
    #     self.assertFalse(Car.objects.filter(id=car.id).exists())


