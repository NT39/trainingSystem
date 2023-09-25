from rest_framework import serializers
from .models import Lesson, LessonView, Product


class LessonViewSerializer(serializers.ModelSerializer):
    view_date = serializers.DateTimeField(source='last_viewed', read_only=True)

    class Meta:
        model = LessonView
        fields = ('lesson', 'status', 'view_time_seconds', 'view_date')


class LessonSerializer(serializers.ModelSerializer):
    lesson_views = LessonViewSerializer(many=True, read_only=True)
    total_views = serializers.IntegerField()
    total_view_time = serializers.IntegerField()
    last_view_date = serializers.DateTimeField()  # Используйте DateTimeField для даты и времени

    class Meta:
        model = Lesson
        fields = ('lesson_name',
                  'video_link',
                  'duration_seconds',
                  'lesson_views',
                  'total_views',
                  'total_view_time',
                  'last_view_date')


class ProductStatsSerializer(serializers.ModelSerializer):
    total_views = serializers.IntegerField()
    total_view_time = serializers.IntegerField()
    total_students = serializers.IntegerField()
    acquisition_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = Product
        fields = ('product_name',
                  'total_views',
                  'total_view_time',
                  'total_students',
                  'acquisition_percentage')
