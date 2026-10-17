from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class AuthenticationBehaviorTests(TestCase):
    fixtures = ["taxi_service_db_data.json"]

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.credentials = {"username": "admin.user", "password": "1qazcde3"}

    def test_every_taxi_view_redirects_anonymous_users_to_login(self):
        for name, args in (
            ("index", []), ("manufacturer-list", []), ("car-list", []),
            ("driver-list", []), ("car-detail", [1]),
            ("driver-detail", [1]),
        ):
            with self.subTest(view=name):
                url = reverse(f"taxi:{name}", args=args)
                self.assertRedirects(
                    self.client.get(url), f"{reverse('login')}?next={url}"
                )

    def test_login_defaults_to_home_and_honors_next(self):
        response = self.client.post(reverse("login"), self.credentials)
        self.assertRedirects(response, reverse("taxi:index"))
        self.client.logout()
        target = reverse("taxi:car-list")
        response = self.client.post(
            reverse("login"), {**self.credentials, "next": target}
        )
        self.assertRedirects(response, target)

    def test_failed_login_and_external_redirect(self):
        response = self.client.post(
            reverse("login"), {**self.credentials, "password": "wrong"}
        )
        self.assertContains(response, "did not match")
        self.assertNotIn("_auth_user_id", self.client.session)
        response = self.client.post(
            reverse("login"),
            {**self.credentials, "next": "https://example.com/"},
        )
        self.assertRedirects(response, reverse("taxi:index"))

    def test_visit_counter_is_per_session_and_pluralized(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:index"))
        self.assertContains(response, "1 time.")
        response = self.client.get(reverse("taxi:index"))
        self.assertContains(response, "2 times.")
        other_client = Client()
        other_client.force_login(self.user)
        response = other_client.get(reverse("taxi:index"))
        self.assertEqual(response.context["num_visits"], 1)

    def test_current_driver_marker_and_sidebar(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertContains(response, "(Me)", count=1)
        self.assertContains(response, self.user.username)
        self.assertContains(response, 'method="post"')
        self.assertContains(
            response, reverse("taxi:driver-detail", args=[self.user.pk])
        )

    def test_logout_requires_post_and_csrf_then_clears_session(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        client.get(reverse("taxi:index"))
        self.assertEqual(client.get(reverse("logout")).status_code, 405)
        self.assertEqual(client.post(reverse("logout")).status_code, 403)
        response = client.post(
            reverse("logout"),
            {"csrfmiddlewaretoken": client.cookies["csrftoken"].value},
        )
        self.assertContains(response, "successfully logged out")
        self.assertTemplateUsed(response, "registration/logged_out.html")
        self.assertNotIn("_auth_user_id", client.session)
        self.assertNotIn("num_visits", client.session)
        self.assertEqual(client.get(reverse("taxi:index")).status_code, 302)
