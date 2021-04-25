import django_filters
from django.shortcuts import get_object_or_404
from rest_framework import mixins, generics
from django_filters.rest_framework import DjangoFilterBackend

from .models import Person, Company
from .serializers import (
    EmployeeSerializer,
    CompanyEmployeeViewValidationSerializer,
    FoodieSeralizer,
    PersonInformationSeralizer,
    PersonFruitsAndVegetablesViewValidationSerializer,
    BlueEyedLivingCommonFriendsViewValidationSerializer,
)


class CompanyEmployeeFilter(django_filters.rest_framework.FilterSet):
    company_id = django_filters.rest_framework.NumberFilter(
        field_name="company__company_id", lookup_expr="exact", label="company_id"
    )


class CompanyEmployeeView(mixins.ListModelMixin, generics.GenericAPIView):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CompanyEmployeeFilter
    queryset = Person.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request, *args, **kwargs):
        validation_serializer_class = CompanyEmployeeViewValidationSerializer(
            data=self.request.query_params
        )
        validation_serializer_class.is_valid(raise_exception=True)
        return self.list(request, *args, **kwargs)


class PersonFruitsAndVegetablesView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CompanyEmployeeFilter
    queryset = Person.objects.all()
    serializer_class = FoodieSeralizer

    def get_object(self):
        filter_kwargs = self.get_object_filter_kwargs
        obj = get_object_or_404(self.queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        validation_serializer_class = PersonFruitsAndVegetablesViewValidationSerializer(
            data=self.request.query_params
        )
        validation_serializer_class.is_valid(raise_exception=True)
        self.get_object_filter_kwargs = dict(self.request.query_params.items())
        return self.retrieve(request, *args, **kwargs)


class BlueEyedLivingCommonFriendsView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = PersonInformationSeralizer

    def get_person(self, index):
        person_field = "person_id"
        guid_field = "guid"
        person_field_index = "{}{}".format(person_field, index)
        guid_field_index = "{}{}".format(guid_field, index)
        person_kwargs = dict()

        for (field, field_index) in (
            (person_field, person_field_index),
            (guid_field, guid_field_index),
        ):
            field_value = self.request.query_params.get(field_index)
            if field_value:
                person_kwargs.update({field: field_value})

        return get_object_or_404(Person.objects.all(), **person_kwargs)

    def get_queryset(self):
        first_person = self.get_person(1)
        second_person = self.get_person(2)
        blue_alive_qs_dict = {"eye_color__name": "blue", "has_died": False}
        first_person_qs = first_person.friends.filter(**blue_alive_qs_dict)
        second_person_qs = second_person.friends.filter(**blue_alive_qs_dict)
        common_friends = first_person_qs.intersection(second_person_qs)
        return common_friends

    def get(self, request, *args, **kwargs):
        validation_serializer_class = (
            BlueEyedLivingCommonFriendsViewValidationSerializer(
                data=self.request.query_params
            )
        )
        validation_serializer_class.is_valid(raise_exception=True)
        return self.list(request, *args, **kwargs)
