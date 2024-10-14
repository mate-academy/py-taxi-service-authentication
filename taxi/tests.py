from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class PrivateTests(TestCase):

    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword123"
        self.user = get_user_model().objects.create_user(
            username=self.username,
            email="test@example.com",
            password=self.password
        )

    class LogInTest(TestCase):
        def setUp(self):
            self.credentials = {
                "username": "admin.user",
                "password": "1qazcde3"
            }
            self.user = get_user_model().objects.create_user(
                username=self.credentials["username"],
                password=self.credentials["password"],
            )

        def test_login(self):
            response = self.client.post(reverse("login"), self.credentials)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(self.client.session.get("_auth_user_id"))
            self.assertTrue(self.user.is_active)

    def test_driver_list_login_required(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('taxi:driver-list')}",
            status_code=302
        )

    def test_car_list_login_required(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('taxi:car-list')}",
            status_code=302
        )

    def test_index_login_required(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('taxi:index')}",
            status_code=302
        )

    def test_car_list(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_driver_list(self):

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
