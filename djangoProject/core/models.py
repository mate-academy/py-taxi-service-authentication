from django.db import models

from django.core.validators import MinValueValidator


# Create your models here.
class Person(models.Model):
    MIN_BIRTH_YEAR = 1900
    full_name = models.CharField(max_length=100)
    birth_year = models.IntegerField(validator=[MinValueValidator(MIN_BIRTH_YEAR)])
    hobby = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name_plural = "people"

    def __str__(self):
        return self.full_name
