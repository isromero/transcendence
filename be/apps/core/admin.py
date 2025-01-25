from django.contrib import admin
from apps.core.models import Users
# Register your models here.

class UserAdmin(admin.ModelAdmin):
	list_display = ('id', 'username', 'email')
	search_fields = ('id', 'username', 'email')

admin.site.register(Users, UserAdmin)



