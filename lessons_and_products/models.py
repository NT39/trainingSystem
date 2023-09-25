from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    username = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.username


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Связь с владельцем продукта.

    def __str__(self):
        return self.product_name


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=255)
    video_link = models.URLField()
    duration_seconds = models.PositiveIntegerField()
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.lesson_name


class LessonView(models.Model):
    STATUS_CHOICES = (
        ('Просмотрено', 'Просмотрено'),
        ('Не просмотрено', 'Не просмотрено'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    view_time_seconds = models.PositiveIntegerField()
    status = models.CharField(max_length=14, choices=STATUS_CHOICES)
    view_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} просмотрел(а) {self.lesson} ({self.status})"


class ProductAccess(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} имеет доступ к {self.product}"
