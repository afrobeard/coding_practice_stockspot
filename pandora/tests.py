import urllib.parse
import random
from itertools import product

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .test_factories import (
    CompanyFactory,
    PersonFactory,
    FruitFactory,
    VegetableFactory,
)


class CompanyEmployeeViewTests(APITestCase):
    def setUp(self):
        self.first_company = CompanyFactory()
        self.second_company = CompanyFactory()
        self.first_company_people = [
            PersonFactory(company=self.first_company) for _ in range(10)
        ]
        self.second_company_people = [
            PersonFactory(company=self.second_company) for _ in range(10)
        ]

    def test_belonging(self):
        url = "{}?{}".format(
            reverse("company_employees"),
            urllib.parse.urlencode({"company_id": self.first_company.company_id}),
        )
        response = self.client.get(url)
        company1_resp_names_set = set([x.get("name") for x in response.data])
        company1_creation_names_set = set([x.name for x in self.first_company_people])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            company1_resp_names_set,
            company1_creation_names_set,
        )

    def test_not_belonging(self):
        url = "{}?{}".format(
            reverse("company_employees"),
            urllib.parse.urlencode({"company_id": self.first_company.company_id}),
        )
        response = self.client.get(url)
        company1_resp_names_set = set([x.get("name") for x in response.data])
        company2_creation_names_set = set([x.name for x in self.second_company_people])

        intersection_set = company1_resp_names_set.intersection(
            company2_creation_names_set
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(intersection_set),
            0,
        )


class PersonFruitsAndVegetablesViewTests(APITestCase):
    def setUp(self):
        self.person = PersonFactory()
        self.fruits = [FruitFactory() for _ in range(random.randint(1, 10))]
        self.vegetables = [VegetableFactory() for _ in range(random.randint(1, 10))]
        self.person.favourite_foods.add(*self.fruits)
        self.person.favourite_foods.add(*self.vegetables)

    def test_lookup_by_person_id(self):
        url = "{}?{}".format(
            reverse("person_fruits_and_vegetables"),
            urllib.parse.urlencode({"person_id": self.person.person_id}),
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lookup_by_guid(self):
        url = "{}?{}".format(
            reverse("person_fruits_and_vegetables"),
            urllib.parse.urlencode({"guid": self.person.guid}),
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fruits_and_vegetables(self):
        url = "{}?{}".format(
            reverse("person_fruits_and_vegetables"),
            urllib.parse.urlencode({"guid": self.person.guid}),
        )
        response = self.client.get(url)
        fruit_set = set([x.name for x in self.fruits])
        vegetables_set = set([x.name for x in self.vegetables])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(response.data.get("fruits")), fruit_set)
        self.assertEqual(set(response.data.get("vegetables")), vegetables_set)


class BlueEyedLivingCommonFriendsViewTests(APITestCase):
    def setUp(self):
        self.first_person = PersonFactory()
        self.second_person = PersonFactory()
        self.match = None

        color_options = ("blue", "brown")
        friend_of_options = ("only_first", "only_second", "both")
        alive_options = (True, False)

        for (color, friend_of, alive) in product(
            color_options, friend_of_options, alive_options
        ):
            friend = PersonFactory(eye_color__name=color, has_died=not alive)
            if friend_of == "only_first":
                self.first_person.friends.add(friend)
            elif friend_of == "only_second":
                self.second_person.friends.add(friend)
            else:
                self.first_person.friends.add(friend)
                self.second_person.friends.add(friend)

            if (color, friend_of, alive) == ("blue", "both", True):
                self.match = friend

    def test_match(self):
        url = "{}?{}".format(
            reverse("blue_eyed_living_common"),
            urllib.parse.urlencode(
                {"guid1": self.first_person.guid, "guid2": self.second_person.guid}
            ),
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        matched_name_from_resp = response.data[0].get("name")
        self.assertEqual(self.match.name, matched_name_from_resp)
