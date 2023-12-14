from django.contrib import admin

from specs.mixins import SeqrchResultsCategory
from .models import *


@admin.register(SpecUnit)
class SpecUnitAdmin(SeqrchResultsCategory, admin.ModelAdmin):
    search_fields = 'name',


@admin.register(SpecCategoryName)
class SpecCategoryNameAdmin(SeqrchResultsCategory, admin.ModelAdmin):
    search_fields = 'name',


admin.site.register(Spec)
admin.site.register(SpecUnitValidation)
admin.site.register(SearchFilterType)
