from django.db import models
import json
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy


# Create your models here.

class Place(models.Model):
    city = models.CharField(max_length=50, blank=False)
    district = models.CharField(max_length=50, blank=False)


def cartypevalidate(value):
    if value not in ['Basic', 'Comfort', 'Premium']:
        raise ValidationError('Wrong type of car input!')


class Car(models.Model):
    brand = models.CharField(max_length=20, blank=False)
    model = models.CharField(max_length=20, blank=False)
    seats = models.CharField(max_length=7, blank=False)
    city_placement = models.CharField(max_length=20, blank=False)
    district_placement = models.CharField(max_length=20, blank=False)
    street_placement = models.CharField(max_length=50, blank=False)

    class CarType(models.TextChoices):
        Basic = 'Basic', gettext_lazy('Basic')
        Comfort = 'Comfort', gettext_lazy('Comfort')
        Premium = 'Premium', gettext_lazy('Premium')

    type = models.CharField(max_length=50,
                            choices=CarType.choices,
                            default=CarType.Basic,
                            blank=False, validators=[cartypevalidate])


class ValidatingPhotos(models.Model):
    photo_before = models.ImageField()
    isin_use = models.BooleanField(default=False, blank=False)
    photo_after = models.ImageField()
    is_used = models.BooleanField()
