from django.contrib import admin

from .models import User, UserConfirmation


class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone_number')


admin.site.register(User, UserModelAdmin)


class UserConfirmationModelAdmin(admin.ModelAdmin):
    list_display = ('code', 'verify_type', 'user')


admin.site.register(UserConfirmation)
