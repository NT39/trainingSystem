from django.urls import path
from . import views

urlpatterns = [
    path('lessons/list', views.LessonListView.as_view(), name='lesson-list'),
    path('lessons/get-by-product/<int:product_id>/',
         views.LessonByProductView.as_view(), name='lesson-by-product'),
    path('products/stats/', views.ProductStatsView.as_view(), name='product-stats'),
]
