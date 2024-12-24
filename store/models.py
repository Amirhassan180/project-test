from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام محصول", null=False)
    description = models.TextField(verbose_name="توضیحات محصول", null=True, blank=True)
    description_all = models.TextField(verbose_name="توضیحات کلی محصول", null=True, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=0, default=0, verbose_name="قیمت", null=False)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="دسته بندی", null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="دسته بندی برند ها", null=True, blank=True)

    image = models.ImageField(upload_to='product_images/', verbose_name="تصویر محصول", null=True, blank=True)
    video_url = models.URLField(max_length=200, verbose_name="لینک ویدئو محصول", null=True, blank=True)

    star = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    is_sale = models.BooleanField(default=False, verbose_name="فروش ویژه")
    sale_price = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="قیمت فروش ویژه",
                                     null=False)
    warehouse = models.IntegerField(default=0, verbose_name="انبار", null=True)

    @property
    def final_price(self):
        """Calculate the final price based on whether the product is on sale or not."""
        if self.is_sale:
            return self.sale_price
        return self.price

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', verbose_name="تصویر محصول")
    is_main = models.BooleanField(default=False, verbose_name="تصویر اصلی")  # Optional: to mark a main image

    def __str__(self):
        return f"{self.product.name} - Image {self.id}"
