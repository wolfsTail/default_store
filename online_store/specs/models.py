from django.db import models

from online_store.main.models import Category


class SearchFilterType(models.Model):
    """_summary_

    """
    CHECKBOX = "checkbox"
    RADIO = "radiobutton"

    HTML_TYPE_CHOICES = (
        (CHECKBOX, "чекбокс"),
        (RADIO, "радиокеопка"),
    )

    key = models.CharField("Ключ поиска", max_length=64, choices=HTML_TYPE_CHOICES,\
                           default=CHECKBOX)
    html_code = models.TextField("HTML-код страницы фильтрации")

    class Meta:
        verbose_name = "Тип поиска при фильтрации"
        verbose_name_plural = "Типы поиска при фильрации"
    
    def __str__(self):
        return f"{self.get_key_display()}"


class SpecCategoryName(models.Model):
    """
    Модель поисковой характеристики в html (')
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    search_filter_type = models.ForeignKey(SearchFilterType, on_delete=models.CASCADE,\
                                           verbose_name="Тип фильтра для поиска")
    name = models.CharField("Название характеристики", max_length=128)
    key = models.CharField("Ключ характеристики", max_length=128)
    use_in_produt_shortlist_specs = models.BooleanField("Используется для отображения в описании твоара", \
                                                        default=False)
    
    class Meta:
        unique_together = ('category', 'name', 'key')
        verbose_name = "Категория характеристик"
        verbose_name_plural = "Категории характеристик"
    
    def __str__(self):
        return f"Хар-ка кат. ->{self.category.title}|{self.name}" 
