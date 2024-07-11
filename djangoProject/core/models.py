from django.db import models


# Create your models here.
class Person(models.Model):
    full_name = models.CharField(max_length=100)
    birth_year = models.IntegerField()
    hobby = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name_plural = "people"

    def __str__(self):
        return self.full_name
