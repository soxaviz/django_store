from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from accounts.models import CustomUser


class Category(models.Model):
    title = models.CharField(
        verbose_name="Название категории",
        max_length=150,
        unique=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Subcategory(models.Model):
    title = models.CharField(
        verbose_name="Название подкатегории",
        max_length=150,
        unique=True
    )
    slug = models.SlugField(
        default="",
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        null=True
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("subcategory_articles", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"


class Product(models.Model):
    objects = None
    title = models.CharField(
        verbose_name="Название продукта",
        max_length=150,
        unique=True)
    slug = models.SlugField(
        default="",
        null=True,
        blank=True
    )
    description = models.TextField(
        verbose_name="Описание"
    )
    price = models.IntegerField(
        verbose_name="Цена",
        default=0
    )
    quantity = models.IntegerField(
        verbose_name="Кол-во продукта",
        default=0)

    views = models.IntegerField(
        verbose_name="Кол-во просмотров",
        default=0
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.SET_NULL,
        verbose_name="Подкатегория",
        null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        null=True
    )

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    def add_to_cart(self):
        return reverse("to_cart", kwargs={"product_id": self.pk, 'action': 'add'})

    def get_first_photo(self):
        photo = self.productimage_set.all().first()
        if photo is not None:
            return photo.photo.url
        return "https://yandex.ru/images/search?pos=1&from=tabbar&img_url=https%3A%2F%2Fzip-perm.com%2Fupload%2Fiblock%2Fdcc%2Fl6abo9tgkfuh6f56hmwyuj3eutbviuq8.jpeg&text=%D0%B7%D0%B4%D0%B5%D1%81%D1%8C+%D1%81%D0%BA%D0%BE%D1%80%D0%BE+%D0%B1%D1%83%D0%B4%D0%B5%D1%82+%D1%84%D0%BE%D1%82%D0%BE&rpt=simage&lr=10335"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductImage(models.Model):
    photo = models.ImageField(
        verbose_name="Фото",
        upload_to="products/",
        null=True,
        blank=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Продукт"
    )


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="reviews",
        null=True,
        blank=True,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
        null=True,
        blank=True,

    )
    content = models.TextField(

    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        blank=True,
        null=True,
        default=0,

    )


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )

    class Meta:
        unique_together = ('user', 'product')
