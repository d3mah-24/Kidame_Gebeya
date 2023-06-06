from django.contrib import admin

from .models import *


@admin.register(MyUser)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "email", "is_staff"]


@admin.register(Products)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["id",
                    "category",
                    "name",
                    "description",
                    "price",
                    "star"]


@admin.register(Cart)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "item"]


@admin.register(Category)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["id",  "name"]
