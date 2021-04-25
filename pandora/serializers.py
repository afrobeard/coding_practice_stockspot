from rest_framework import serializers
from .models import Person, Tag, Company, Food
from .model_choices import FoodChoices


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]

    def to_representation(self, instance):
        return instance.name


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ["name"]

    def to_representation(self, instance):
        return instance.name


class EmployeeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    company_id = serializers.SerializerMethodField()

    def get_company_id(self, employee):
        return employee.company and employee.company.company_id

    class Meta:
        model = Person
        fields = ["name", "email", "address", "gender", "tags", "company_id"]


class PersonInformationSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["name", "age", "address", "phone"]


class FoodieSeralizer(serializers.ModelSerializer):
    fruits = serializers.SerializerMethodField(read_only=True)
    vegetables = serializers.SerializerMethodField(read_only=True)

    def get_fruits(self, person):
        return FoodSerializer(
            person.favourite_foods.filter(type=FoodChoices.FRUIT), many=True
        ).data

    def get_vegetables(self, person):
        return FoodSerializer(
            person.favourite_foods.filter(type=FoodChoices.VEGETABLE), many=True
        ).data

    class Meta:
        model = Person
        fields = ["username", "age", "fruits", "vegetables"]


class CompanyEmployeeViewValidationSerializer(serializers.Serializer):
    company_id = serializers.IntegerField(required=True, min_value=0)

    def validate_company_id(self, company_id):
        if not Company.objects.filter(company_id=company_id).exists():
            raise serializers.ValidationError("Company ID inexistent")

        return company_id


class PersonFruitsAndVegetablesViewValidationSerializer(serializers.Serializer):
    person_id = serializers.IntegerField(min_value=0, required=False)
    guid = serializers.UUIDField(required=False)

    def validate(self, data):
        if not (data.get("person_id") or data.get("guid")):
            raise serializers.ValidationError("Supply one of person_id or guid")
        return data


class BlueEyedLivingCommonFriendsViewValidationSerializer(serializers.Serializer):
    person_id1 = serializers.IntegerField(min_value=0, required=False)
    guid1 = serializers.UUIDField(required=False)
    person_id2 = serializers.IntegerField(min_value=0, required=False)
    guid2 = serializers.UUIDField(required=False)

    def validate(self, data):
        if not (data.get("person_id1") or data.get("guid1")):
            raise serializers.ValidationError("Supply one of person_id1 or guid1")
        if not (data.get("person_id2") or data.get("guid2")):
            raise serializers.ValidationError("Supply one of person_id2 or guid2")
        return data
