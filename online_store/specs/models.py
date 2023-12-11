from django.db import models

from main.models import Category


class SearchFilterType(models.Model):
    """
    Модель фильра страницы
    """
    CHECKBOX = "checkbox"
    RADIO = "radiobutton"

    HTML_TYPE_CHOICES = (
        (CHECKBOX, "чекбокс"),
        (RADIO, "радиокнопка"),
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


class Spec(models.Model):
    """
    Непосредственно характеристика
    """
    INT = "int"
    STR = "str"
    FLOAT = "float"
    BOOL = "bool"

    TYPE_CHOICES = (
        (INT, "Целое число"),
        (STR, "Стррока"),
        (FLOAT, "Число с плавающей точкой"),
        (BOOL, "Логический тип"),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE,\
                                  verbose_name="Категория характеристик",\
                                    related_name="category_specs")
    spec_category = models.ForeignKey(SpecCategoryName, on_delete=models.CASCADE,\
                                      verbose_name="Наименование категории характеристики",\
                                        related_name="specnames")
    product = models.ForeignKey("main.Product", on_delete=models.CASCADE, verbose_name="Товар",\
                                related_name="product_specs", null=True, blank=True)
    spec_unit = models.ForeignKey("SpecUnit", on_delete=models.CASCADE, verbose_name="Единица измерения",\
                                   null=True, blank=True)
    value = models.CharField("Значение характеристики", max_length=64)
    var_type = models.CharField("Тип значения", max_length=32, choices=TYPE_CHOICES, null=True,\
                                blank=True)
    
    class Meta:
        unique_together = ('category', 'spec_category', 'product', 'value')
        verbose_name = "Характеристика товара"
        verbose_name_plural = "Характеристики товаров"

    def __str__(self) -> str:
        return "|".join(
            self.category.title,
            self.spec_category.name,
            self.spec_category.key,
            self.value,
        )


class SpecUnit(models.Model):
    """
    Единица измерения характеристики
    """

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория характеристики")
    name = models.CharField('Наименование величины', max_length=128)
    unit = models.CharField('Единица измерения', max_length=16)

    class Meta:
        unique_together = ('category', 'name', 'unit')
        verbose_name = "Единица измерения характеристики"
        verbose_name_plural = "Еденицы измерения характеристик"
    
    def __str__(self) -> str:
        return f"Единица измерения - {self.category.title}|{self.name}|{self.unit}"
    

class SpecUnitValidation(models.Model):
    """
    Модель для валидации характеристик по типу значения
    """
    INT = "int"
    STR = "str"
    FLOAT = "float"
    BOOL = "bool"

    TYPE_CHOICES = (
        (INT, "Целое число"),
        (STR, "Стррока"),
        (FLOAT, "Число с плавающей точкой"),
        (BOOL, "Логический тип"),
    )

    specunit = models.ForeignKey(SpecUnit, on_delete=models.CASCADE, verbose_name="Единица измерения")
    name = models.CharField('Наименование величины', max_length=128)
    var_type = models.CharField('Тип величины характеристики', max_length=32, choices=TYPE_CHOICES)

    class Meta:
        unique_together = ('specunit', 'name', 'var_type')
        verbose_name = "Единицы измерения при валидации"
        verbose_name_plural = "Единицы измерения при валидации"
    
    def __str__(self) -> str:
        return f"Валидация {self.spec_unit}"


