from typing import Any
from django.contrib import admin
from django.db.models.fields.related import ForeignKey
from django.forms.models import ModelChoiceField
from django.http.request import HttpRequest
from django.utils.safestring import mark_safe

from specs.models import Spec
from .models import *


class AdditionalProductImageTabularInLine(admin.TabularInline):
    model = AdditionalProductImage
    extra = 1

class SpecsTabularInline(admin.TabularInline):
    model = Spec
    extra = 1

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
