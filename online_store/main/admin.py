from typing import Any
from django.contrib import admin
from django.db.models.fields.related import ForeignKey
from django.forms import BaseInlineFormSet, ValidationError
from django.forms.models import ModelChoiceField
from django.http.request import HttpRequest
from django.utils.safestring import mark_safe

from specs.models import Spec, SpecUnitValidation
from .models import *


class AdditionalProductImageTabularInLine(admin.TabularInline):
    model = AdditionalProductImage
    extra = 1


class SpecsProductInLineFormSet(BaseInlineFormSet):
    def clean(self):
        data = getattr(self, 'cleaned_data', None)
        if not data:
            return super().clean()
        spec_categories_id = []
        for item in data:
            if item.get('spec_unit'):
                validation = SpecUnitValidation.objects.filter(specunit=item['spec_unit']).first()
                if validation:
                    if item['var_type'] != validation.var_type:
                        raise ValidationError(
                            f"Несоответствие типа значения характеристики {item['spec_unit'].name}.\
                                Ожидается {validation.get_var_type_display()}."
                        )
            if item.get('spec_category'):
                spec_categories_id.append(item['spec_category'].id)
        if spec_categories_id:
            if len(spec_categories_id) != len(set(spec_categories_id)):
                raise ValidationError("Присутсвуют дублирующие категории характеристик!")

        super().clean()



class SpecsTabularInline(admin.TabularInline):
    model = Spec
    extra = 1
    autocomplete_fields = "spec_category", "spec_unit",
    formset = SpecsProductInLineFormSet

    def formfield_for_foreignkey(self, db_field: ForeignKey[Any], request: HttpRequest | None, **kwargs: Any) -> ModelChoiceField | None:
        product_id = request.resolver_match.kwargs.get('object_id')
        if product_id:
            product = Product.objects.get(id=product_id)
            if db_field.name == "category":
                kwargs['queryset'] = Category.objects.filter(id=product.category.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'price', 'get_image',)
    inlines = [SpecsTabularInline, AdditionalProductImageTabularInLine]

    @admin.display(description='Изображение')
    def get_image(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' style='margin: auto;\
                              width: auto;' height='100px;'")
        return ""



admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
