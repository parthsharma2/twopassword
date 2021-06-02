from twopassword import passwords
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.test import TestCase
from django.urls import reverse

from twopassword.passwords.encryptor import Encryptor
from twopassword.passwords.models import Password


class AddPasswordTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("johnDoe", password="secret-password")
        self.client.login(username="johnDoe", password="secret-password")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/passwords/add")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("add-password"))
        self.assertEqual(response.status_code, 200)

    def test_view_shows_form_to_add_password(self):
        response = self.client.get(reverse("add-password"))
        self.assertTemplateUsed(response, "passwords/add.html")

    def test_view_shows_success_message_on_submission(self):
        response = self.client.post(
            reverse("add-password"),
            data={
                "website_name": "test website",
                "website_address": "www.website.com",
                "username": "testusername",
                "password": "testpassword",
            },
        )
        self.assertTemplateUsed(response, "passwords/add_success.html")

    def test_redirects_unauthenticated_users(self):
        self.client.logout()
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)


class DeletePasswordTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("johnDoe", password="secret-password")
        self.client.login(username="johnDoe", password="secret-password")

        self.password = Password.objects.create(
            website_name="Test Website",
            website_address="www.testwebsite.com",
            username="testusername",
            password="testpassword",
            owner=self.user,
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f"/passwords/delete/{self.password.id}")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("delete-password", args=[self.password.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_shows_confirmation_page(self):
        response = self.client.get(reverse("delete-password", args=[self.password.id]))
        self.assertTemplateUsed(response, "passwords/delete.html")

    def test_view_prevents_non_owner_from_deleting(self):
        self.password.owner = User.objects.create(
            username="testUser", password="secret-password"
        )
        self.password.save()
        response = self.client.post(reverse("delete-password", args=[self.password.id]))
        self.assertEqual(response.status_code, 403)

    def test_view_shows_success_page_on_delete(self):
        self.password.owner = self.user
        self.password.save()
        response = self.client.post(reverse("delete-password", args=[self.password.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "passwords/delete_success.html")

    def test_view_returns_a_404_if_id_is_not_present(self):
        response = self.client.post(reverse("delete-password", args=[101]))
        self.assertEqual(response.status_code, 404)

    def test_redirects_unauthenticated_users(self):
        self.client.logout()
        response = self.client.get(reverse("delete-password", args=[self.password.id]))
        self.assertEqual(response.status_code, 302)


class ShowPasswordViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("johnDoe", password="secret-password")
        self.client.login(username="johnDoe", password="secret-password")

        e = Encryptor()
        self.decrypted_password = "testpass"
        self.encrypted_password = e.encrypt(self.decrypted_password)

        self.password = Password.objects.create(
            website_name="Test Website",
            website_address="www.testwebsite.com",
            username="testusername",
            password=self.encrypted_password,
            owner=self.user,
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f"/passwords/show/{self.password.id}")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("show-password", args=[self.password.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_show_password_verification_template(self):
        response = self.client.get(reverse("show-password", args=[self.password.id]))
        self.assertTemplateUsed(response, "passwords/verification.html")

    def test_view_shows_password_details_on_correct_password(self):
        response = self.client.post(
            reverse("show-password", args=[self.password.id]),
            data={"password": "secret-password"},
        )

        self.assertTemplateUsed(response, "passwords/show.html")

    def test_view_shows_decrypted_password_on_correct_password(self):
        response = self.client.post(
            reverse("show-password", args=[self.password.id]),
            data={"password": "secret-password"},
        )

        self.assertEqual(response.context["obj"].password, self.decrypted_password)

    def test_view_returns_a_404_if_id_is_not_present(self):
        response = self.client.post(
            reverse("show-password", args=[101]), data={"password": "secret-password"}
        )

        self.assertEqual(response.status_code, 404)

    def test_redirects_unauthenticated_users(self):
        self.client.logout()
        response = self.client.get(reverse("show-password", args=[self.password.id]))
        self.assertEqual(response.status_code, 302)


class GeneratePasswordViewTest(TestCase):
    def setUp(self):
        User.objects.create_user("johnDoe", password="secret-password")
        self.client.login(username="johnDoe", password="secret-password")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/passwords/generate")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("generate-password"))
        self.assertEqual(response.status_code, 200)

    def test_view_returns_json_response(self):
        response = self.client.get(reverse("generate-password"))
        self.assertEqual(type(response), JsonResponse)

    def test_view_returns_a_fifteen_character_password(self):
        response = self.client.get(reverse("generate-password"))
        password = response.json()["password"]

        self.assertEqual(len(password), 15)

    def test_view_returns_a_random_password(self):
        response = self.client.get(reverse("generate-password"))
        password = response.json()["password"]
        response = self.client.get(reverse("generate-password"))
        new_password = response.json()["password"]

        self.assertNotEqual(password, new_password)

    def test_redirects_unauthenticated_users(self):
        self.client.logout()
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)


class PasswordListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 15 passwords
        user = User.objects.create_user("johnDoe", password="secret-password")

        for i in range(15):
            Password.objects.create(
                website_name=f"Website {i}",
                website_address=f"www.website{i}.com",
                username=f"john{i}",
                password=f"pass{i}",
                owner=user,
            )

    def setUp(self):
        self.client.login(username="johnDoe", password="secret-password")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("dashboard"))
        self.assertTemplateUsed(response, "passwords/dashboard.html")

    def test_pagination_is_five(self):
        response = self.client.get(reverse("dashboard"))
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["page_obj"]), 5)

    def test_redirects_unauthenticated_users(self):
        self.client.logout()
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
