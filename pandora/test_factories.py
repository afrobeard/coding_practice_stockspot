import factory
import uuid
import random
from django.utils import timezone
from .models import Company, Person, Color, Food
from .model_choices import GenderChoices, FoodChoices


class VegetableFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "Vegetable{}".format(n))
    type = FoodChoices.VEGETABLE

    class Meta:
        model = Food


class FruitFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "Fruit{}".format(n))
    type = FoodChoices.FRUIT

    class Meta:
        model = Food


class ColorFactory(factory.django.DjangoModelFactory):
    name = "black"

    class Meta:
        model = Color
        django_get_or_create = ("name",)


class TagFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "Tag{}".format(n))

    class Meta:
        model = Color


class CompanyFactory(factory.django.DjangoModelFactory):
    company_id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: "Company{}".format(n))

    class Meta:
        model = Company


class PersonFactory(factory.django.DjangoModelFactory):
    guid = factory.Sequence(lambda n: uuid.uuid4())
    person_id = factory.Sequence(lambda n: n)
    eye_color = factory.SubFactory(ColorFactory)
    registered = factory.LazyFunction(timezone.now)
    gender = GenderChoices.NONBINARY
    has_died = False
    name = factory.Sequence(lambda n: "John{} Doe{}".format(n, n))
    email = factory.Sequence(lambda n: "JohnDoe{}@example.com".format(n))
    address = factory.Sequence(
        lambda n: "{} Sumner Place, Sperryville, American Samoa, 9819".format(n)
    )
    birth_year = factory.Sequence(lambda n: random.randint(1950, 1990))
    company = factory.SubFactory(CompanyFactory)

    class Meta:
        model = Person
