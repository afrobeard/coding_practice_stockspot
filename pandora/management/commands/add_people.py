import os
import csv
import dateparser
import ijson
from collections import defaultdict
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from pandora.models import Person, Color, Food, Tag, Company
from pandora.model_choices import FoodChoices


class Command(BaseCommand):
    help = """Loads countries into database in Pandora Country Format"""

    def add_arguments(self, parser):
        parser.add_argument("--json_file", dest="json_file", help="Country JSON File")

    def add_tags(self, person_obj, person):
        tag_objs = list()
        for tag in person.get("tags"):
            (tag_obj, _) = Tag.objects.get_or_create(name=tag)
            tag_objs.append(tag_obj)
        person_obj.tags.add(*tag_objs)

    def load_fruits_and_vegetables_categories(self):
        with open("fruit_classification.csv") as csvfile:
            reader = csv.DictReader(csvfile)
            items = [(row.get("name"), row.get("type")) for row in reader]
            self.vegetables_set = set(
                [
                    name
                    for (name, food_type) in items
                    if food_type == FoodChoices.VEGETABLE
                ]
            )
            self.fruits_set = set(
                [name for (name, food_type) in items if food_type == FoodChoices.FRUIT]
            )

    def add_food(self, person_obj, person):
        food_objs = list()
        for food in person.get("favouriteFood"):
            food_obj = Food.objects.filter(name=food).first()
            if food_obj is None:
                if food in self.fruits_set:
                    food_type = FoodChoices.FRUIT
                elif food in self.vegetables_set:
                    food_type = FoodChoices.VEGETABLE
                else:
                    raise ValueError("Unknown Food Type")
                food_obj = Food.objects.create(name=food, type=food_type)
            food_objs.append(food_obj)
        person_obj.favourite_foods.add(*food_objs)

    @transaction.atomic
    def handle(self, *args, **options):
        self.load_fruits_and_vegetables_categories()
        json_file_path = options.get("json_file")

        if not json_file_path:
            self.stdout.write(self.style.ERRROR("JSON File not Specified"))
            exit(0)

        try:
            os.stat(json_file_path)
        except FileNotFoundError:
            self.stdout.write(self.style.ERRROR("JSON File doesnt Exist"))
            exit(0)

        friend_relationships = defaultdict(lambda: list())

        with open(json_file_path) as f:
            persons = ijson.items(f, "item")
            for person in persons:
                person_id = person.get("index")

                for friend_obj in person.get("friends"):
                    friend_id = friend_obj.get("index")
                    friend_relationships[person_id].append(friend_id)

                age = person.get("age")
                eye_color = person.get("eyeColor")
                (eye_color_obj, _) = Color.objects.get_or_create(name=eye_color)
                company_id = person.get("company_id")
                company_obj = Company.objects.get(company_id=company_id)
                birth_year = timezone.now().year - age
                registered_date = dateparser.parse(person.get("registered"))
                data = {
                    "guid": person.get("guid"),
                    "person_id": person_id,
                    "has_died": person.get("has_died"),
                    "balance": person.get("balance", "").strip("$").replace(",", ""),
                    "picture": person.get("picture"),
                    "birth_year": birth_year,  # COMPUTED FROM AGE
                    "eye_color": eye_color_obj,
                    "name": person.get("name"),
                    "gender": person.get("gender"),
                    "company": company_obj,
                    "email": person.get("email"),
                    "phone": person.get("phone"),
                    "address": person.get("address"),
                    "about": person.get("about"),
                    "registered": registered_date,
                    "greeting": person.get("greeting"),
                }

                person_obj = Person.objects.create(**data)
                self.add_tags(person_obj, person)
                self.add_food(person_obj, person)

        for (person_id, friend_ids) in friend_relationships.items():
            person = Person.objects.get(person_id=person_id)
            person.friends.add(*Person.objects.filter(person_id__in=friend_ids))
