from django.db import models
from decimal import Decimal
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from .model_choices import GenderChoices, FoodChoices


class Color(models.Model):
    name = models.CharField(null=True, max_length=50, db_index=True)


class Food(models.Model):
    name = models.CharField(null=True, max_length=50, db_index=True)
    type = models.CharField(null=False, max_length=10, choices=FoodChoices.choices)


class Tag(models.Model):
    name = models.CharField(null=True, max_length=50, db_index=True)


# Create your models here.
class Company(models.Model):
    company_id = models.PositiveIntegerField(null=False)
    name = models.CharField(max_length=200, db_index=True, null=False)


class Person(models.Model):
    """
    Friends are unidirectional
    e.g.
    index 20 has index 18 in their friends
    index 18 does not have index 20 in their friends
    """

    guid = models.UUIDField(null=False, db_index=True, unique=True)
    person_id = models.PositiveIntegerField(null=False, unique=True, db_index=True)
    has_died = models.BooleanField(default=False, null=False)
    balance = models.DecimalField(
        default=Decimal(0), max_digits=10, decimal_places=2, null=False
    )
    picture = models.URLField()
    birth_year = models.PositiveIntegerField(null=False)
    eye_color = models.ForeignKey(Color, null=False, on_delete=models.PROTECT)
    name = models.CharField(null=False, max_length=200)
    gender = models.CharField(null=False, max_length=10, choices=GenderChoices.choices)
    company = models.ForeignKey(Company, null=False, on_delete=models.PROTECT)
    email = models.EmailField(null=False)
    phone = PhoneNumberField(null=False)
    address = models.CharField(null=False, max_length=200)
    about = models.CharField(null=True, max_length=1000)
    registered = models.DateTimeField(null=False)
    friends = models.ManyToManyField("Person")
    tags = models.ManyToManyField(Tag)
    greeting = models.CharField(default=False, max_length=200)
    favourite_foods = models.ManyToManyField(Food)

    @property
    def age(self):
        return timezone.now().year - self.birth_year

    @property
    def username(self):
        return self.email
