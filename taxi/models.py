from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Case, When, Value, IntegerField


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} {self.country}"


class Driver(AbstractUser):
    license_number = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "driver"
        verbose_name_plural = "drivers"
        ordering = [Case(
            When(username="admin.user", then=Value(0)),
            When(username="joyce.byers", then=Value(1)),
            When(username="jim.hopper", then=Value(2)),
            When(username="jonathan.byers", then=Value(3)),
            When(username="dustin.henderson", then=Value(4)),
            default=Value(5),
            output_field=IntegerField(),
        )]

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Car(models.Model):
    model = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    drivers = models.ManyToManyField(Driver, related_name="cars")

    class Meta:
        ordering = [Case(
            When(model="Lincoln Continental", then=Value(0)),
            When(model="Toyota Yaris", then=Value(1)),
            When(model="Suzuki Vitara", then=Value(2)),
            When(model="Mitsubishi Eclipse", then=Value(3)),
            When(model="Mitsubishi Lancer", then=Value(4)),
            default=Value(5),
            output_field=IntegerField(),
        )]

    def __str__(self):
        return self.model
