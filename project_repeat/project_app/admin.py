from django.contrib import admin

from .models import CustomUser,Blog,Comment

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Blog)
admin.site.register(Comment)