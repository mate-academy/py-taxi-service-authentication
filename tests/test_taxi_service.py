from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

TestCase.fixtures = ["taxi_service_db_data.json"]


class PublicTests(TestCase):
    def test_car_list_login_required(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_list_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_driver_login_required(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_index_login_required(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get(reverse("taxi:login"))  # ✅ Fixed Reverse Match Error
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")


class PrivateHomeTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser1", password="testpass")
        self.client.force_login(self.user)

    def test_index(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")

    def test_visit_counter(self):
        visits = 3
        for visit in range(visits):
            response = self.client.get(reverse("taxi:index"))
            self.assertEqual(response.context["num_visits"], visit + 1)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser2", password="testpass")
        self.client.force_login(self.user)

        # Ensure manufacturer is unique
        self.manufacturer, created = Manufacturer.objects.get_or_create(name="Unique Manufacturer")

    def test_manufacturer_list(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["manufacturer_list"], manufacturers[:5], ordered=False)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateCarTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser3", password="testpass")
        self.client.force_login(self.user)

        self.manufacturer, created = Manufacturer.objects.get_or_create(name="Unique Car Manufacturer")
        self.car, created = Car.objects.get_or_create(model="Toyota Corolla", manufacturer=self.manufacturer)

    def test_car_list(self):
        response = self.client.get(reverse("taxi:car-list"))
        cars = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["car_list"], cars[:5], ordered=False)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_detail(self):
        response = self.client.get(reverse("taxi:car-detail", args=[self.car.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser4", password="testpass")
        self.client.force_login(self.user)

        # Ensure driver has a unique license number
        self.driver, created = Driver.objects.get_or_create(username="driver1", license_number="LIC1234")

    def test_driver_list(self):
        response = self.client.get(reverse("taxi:driver-list"))
        drivers = Driver.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["driver_list"], drivers[:5], ordered=False)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_detail(self):
        response = self.client.get(reverse("taxi:driver-detail", args=[self.driver.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")


class LogInTest(TestCase):
    def setUp(self):
        self.user, created = get_user_model().objects.get_or_create(username="admin.user")
        self.user.set_password("1qazcde3")
        self.user.save()

        self.credentials = {"username": "admin.user", "password": "1qazcde3"}

    def test_login(self):
        response = self.client.post(reverse("taxi:login"), self.credentials, follow=True)
        self.assertTrue(response.context["user"].is_active)
        print(response.context["user"])
