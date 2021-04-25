from django.contrib import admin
from .models import Color, Food, Tag, Company, Person

# Register your models here.


class LookupModelAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("id", "name")


class FoodModelAdmin(admin.ModelAdmin):
    search_fields = ("name", "type")
    list_display = ("id", "name", "type")
    list_filter = ("type",)


class CompanyModelAdmin(admin.ModelAdmin):
    search_fields = ("id", "company_id", "name")
    list_display = ("id", "company_id", "name")


class PersonModelAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "guid")
    list_display = ("id", "person_id", "guid", "name", "has_died")
    list_filter = ("has_died",)


admin.site.register(Color, LookupModelAdmin)
admin.site.register(Food, FoodModelAdmin)
admin.site.register(Tag, LookupModelAdmin)
admin.site.register(Person, PersonModelAdmin)
admin.site.register(Company, CompanyModelAdmin)
