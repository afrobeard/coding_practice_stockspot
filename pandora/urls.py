from django.conf import settings
from django.urls import path, include
from .views import (
    CompanyEmployeeView,
    PersonFruitsAndVegetablesView,
    BlueEyedLivingCommonFriendsView,
)

urlpatterns = [
    path("company_employees/", CompanyEmployeeView.as_view(), name="company_employees"),
    path(
        "person_fruits_and_vegetables/",
        PersonFruitsAndVegetablesView.as_view(),
        name="person_fruits_and_vegetables",
    ),
    path(
        "blue_eyed_living_common/",
        BlueEyedLivingCommonFriendsView.as_view(),
        name="blue_eyed_living_common",
    ),
]
