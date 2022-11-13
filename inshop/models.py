from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class SuperUser(BaseUserManager):
    def create_user(self, username, email, **extra_fields):
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.user_type = 'admin'
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username"]

    objects = SuperUser()

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["username", ]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название", unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        ordering = ["name", ]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заглавие")
    description = models.TextField(verbose_name="Описание")
    created = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to="product/%Y/%m/%d/", blank=True, null=True, verbose_name="Картинка")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    discount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Скидка", blank=True, null=True)
    supplier = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")

    class Meta:
        ordering = ["created"]
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.title


class Comment(models.Model):
    rates = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    rate = models.IntegerField(choices=rates, blank=True, null=True, verbose_name="Оценка")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    content = models.TextField(blank=True, verbose_name="Содержание")
    created = models.DateTimeField(auto_now_add=True)
    replies = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, verbose_name="Ответы")

    class Meta:
        ordering = ["created"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"Author: {self.author} Product: {self.product}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.FloatField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    is_order = models.BooleanField(default=False)

    class Meta:
        ordering = ["created"]
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"

    def __str__(self):
        return f"Cart {self.id}"


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart", verbose_name="Корзина")
    quantity = models.IntegerField(default=1)
    cart_item_price = models.FloatField(default=0)

    class Meta:
        ordering = ["cart_item_price"]
        verbose_name = "Выбранные продукты"
        verbose_name_plural = "Выбранные продукты"

    def __str__(self):
        return f"Продукт: {self.product} Количество: {self.quantity}"

    def save(self, *args, **kwargs):
        self.cart_item_price = self.quantity * self.product.price
        super().save(*args, **kwargs)


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.FloatField(default=0, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created"]
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Покупатель: {self.user} Total price: {self.total_price}"
