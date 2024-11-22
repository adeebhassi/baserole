from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from .models import User, Role

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email','get_roles_display')
   
    search_fields = ('username', 'email')

    

admin.site.register(User, UserAdmin)
admin.site.register(Role)  # Ensure roles are registered so they can be selected
