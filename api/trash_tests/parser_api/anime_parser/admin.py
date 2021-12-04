from django.contrib import admin

from . import models


class UsersAdmin(admin.ModelAdmin):
    list_display = ["pk", "user_id", "user_name", "first_name", "last_name"]
    list_editable = ["user_id", "user_name", "first_name", "last_name"]

admin.site.register(models.TelegramUsers, UsersAdmin)