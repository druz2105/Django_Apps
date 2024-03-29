from django.contrib import admin
from .models import User, UserProfileImages, UserSubscription
from django.utils.translation import gettext_lazy as _


# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    readonly_fields = ('password',)  # make password field readonly

    fieldsets = (
        (None, {'fields': ('password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'customer_id')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ('customer_id',)

    def password(self, obj):
        return '********'  # display asterisks instead of the actual password

    password.short_description = _('Password')


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfileImages)
admin.site.register(UserSubscription)
