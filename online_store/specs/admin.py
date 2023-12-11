from django.contrib import admin

from .models import *


admin.site.register(Spec)
admin.site.register(SpecUnit)
admin.site.register(SpecCategoryName)
admin.site.register(SpecUnitValidation)
admin.site.register(SearchFilterType)
