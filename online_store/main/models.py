from slugify import slugify

from django.conf import settings
from django.db import models

from utils.image_uploaders import product_image_upload


class Category(models.Model):

    title = models.CharField("Наименование категории", max_length=64, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товаров"

    def __str__(self) -> str:
        return f"{self.title} | {self.id}"


class Brand(models.Model):

    title = models.CharField("Наименование производителя", max_length=128)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")

    class Meta:
        verbose_name = "Производитель товара"
        unique_together = ("title", "category")
        
    def __str__(self):
        return f"{self.title} |Category - {self.category.title}"


class Product(models.Model):
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE,\
                                 verbose_name="Наименование категории", related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,\
                               verbose_name="Производитель товара", related_name="brand_products")
    title = models.CharField("Наименование продукта", max_length=128)
    image = models.ImageField('Изображение', upload_to=product_image_upload, blank=True, null=True)
    slug = models.SlugField(unique=True)
    price = models.DecimalField("Стоимость", max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ("category", "title", "slug")
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.title} | {self.category.title}"


class AdditionalProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    image = models.ImageField(upload_to=product_image_upload, blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        verbose_name = "Дополнительная иллюстрация твоара"
        verbose_name_plural = "Дополнительные иллюстрации товара"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.product.slug)
        return super().save(*args, **kwargs)


class Customer(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, \
                                verbose_name="Покупатель")
    phone = models.CharField("Номер телефона", max_length=13, blank=True)
    address = models.TextField(blank=True)

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"

    def __str__(self):
        return f"Покупатель - {self.user.email}"


class Cart(models.Model):

    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Владалец")
    items = models.ManyToManyField("CartItem", verbose_name="Товары", related_name="items_of_cart")
    total_cost = models.DecimalField("Общая стоимость", max_digits=11, decimal_places=2)
    in_order = models.BooleanField(default=False, verbose_name="Использован?")

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Заказ покупателя - {self.owner.email}"


class CartItem(models.Model):

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="Корзина",\
                              related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    qty = models.IntegerField('Количество товара', default=1)
    total_cost = models.DecimalField("Итого", max_digits=11, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
    
    def __str__(self):
        return f"{self.id} | {self.product.title}|корзина->№{self.cart.id}"


class Order(models.Model):

    NEW = "new"
    IN_PROGRESS = "in_progress"
    IS_READY = "is_ready"
    COMPLETED = "completed"
    ON_THE_WAY = "on_the_way"
    DELIVERED = "delivered"
    DEFAULT = "default"

    STATUS_CHOICES = (
        (NEW, "Новый"),
        (IN_PROGRESS, "В обработке"),
        (IS_READY, "Собран"),
        (COMPLETED, "Завершен"),
        (ON_THE_WAY, "В пути"),
        (DELIVERED, "Доставлен"),
        (DEFAULT, "неопределён")
    )

    BUYING_TYPE_SELF = "self"
    BUYING_TYPE_DELIVERY = "delivery"
    BUYING_TYPE_DEFAULT = "default"

    BUYING_CHOICES = (
        (BUYING_TYPE_SELF, "Самовывоз"),
        (BUYING_TYPE_DELIVERY, "Доставка"),
        (BUYING_TYPE_DEFAULT, "Неопределён")
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,\
                                verbose_name="Покупатель")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="Корзина")
    status = models.CharField("Стутус заказа", max_length=32, choices=STATUS_CHOICES,\
                              default=NEW)
    comment = models.TextField("Комментарий к заказу", blank=True)
    order_cost = models.DecimalField("Стоимость заказа", max_digits=11, decimal_places=2)
    order_date = models.DateField("Дата заказа", null=True, blank=True)
    created = models.DateTimeField("Дата создания заказа", auto_now_add=True)
    buying_type = models.CharField("Тип заказа", choices=BUYING_CHOICES, default=BUYING_TYPE_SELF)
    phone = models.CharField("Номер телефона", max_length=13)
    first_name = models.CharField("Имя", max_length=64)
    last_name = models.CharField("Фамилия", max_length=64)
    address = models.CharField("Адрес доставки", max_length=128, null=True, blank=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ №{self.id}|Покупатель-{self.customer.user.email}"
