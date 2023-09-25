from django.contrib import admin
from lessons_and_products.models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(Lesson)
admin.site.register(LessonView)
admin.site.register(ProductAccess)
