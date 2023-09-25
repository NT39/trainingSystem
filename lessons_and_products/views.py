from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from .models import Lesson, LessonView, Product, CustomUser
from .serializers import LessonSerializer, ProductStatsSerializer
from django.db.models import Count, Case, When, Sum, IntegerField, Max, F, DateTimeField, \
    ExpressionWrapper, DecimalField


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user

        queryset = Lesson.objects.filter(
            products__productaccess__user=user
        ).annotate(
            total_views=Count('lessonview', distinct=True),
            total_view_time=Sum(
                Case(
                    When(lessonview__status='Просмотрено', then='lessonview__view_time_seconds'),
                    default=0,
                    output_field=IntegerField()
                )
            ),
            last_view_date=Max(
                Case(
                    When(lessonview__status='Просмотрено', then='lessonview__view_date'),
                    default=None,
                    output_field=DateTimeField()
                )
            )
        )

        return queryset


class LessonByProductView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs['product_id']

        # Получаем дату последнего просмотра для каждого урока
        last_view_dates = LessonView.objects.filter(
            user=user,
            lesson__products__productaccess__product_id=product_id,
            status='Просмотрено'
        ).values('lesson_id').annotate(
            last_view_date=Max('view_date')
        )

        # Получаем остальные данные об уроках
        queryset = Lesson.objects.filter(
            products__productaccess__user=user,
            products__id=product_id
        ).annotate(
            total_views=Count('lessonview', distinct=True),
            total_view_time=Sum(
                Case(
                    When(lessonview__status='Просмотрено', then='lessonview__view_time_seconds'),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )

        # Объединяем данные
        queryset = queryset.annotate(
            last_view_date=Case(
                When(id__in=[item['lesson_id'] for item in last_view_dates], then=F('lessonview__view_date')),
                default=None,
                output_field=DateTimeField()
            )
        )

        return queryset


class ProductStatsView(generics.ListAPIView):
    serializer_class = ProductStatsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        products = Product.objects.all()

        queryset = products.annotate(
            total_views=Count('lesson__lessonview', distinct=True),
            total_view_time=Sum('lesson__lessonview__view_time_seconds'),
            total_students=Count('productaccess__id', distinct=True),  # Используем поле id
            acquisition_percentage=ExpressionWrapper(
                Count('productaccess', distinct=True) * 100.0 / CustomUser.objects.count(),
                output_field=DecimalField(max_digits=5, decimal_places=2)
            )
        )

        return queryset
