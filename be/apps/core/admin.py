from django.contrib import admin
from apps.core.models import Users
# Register your models here.

class UserAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'email')
	search_fields = ('nombre', 'email')

admin.site.register(Users, UserAdmin)