from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, Student

class UserConfig(UserAdmin):
    model = User

    list_filter = ('email', 'username', 'is_active', 'is_staff')
    ordering = ('-date_joined',)
    list_display = ('email', 'username',
                    'is_active', 'is_staff')

    fieldsets = (
        ("User Information", {'fields': ('email', 'username')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )

class StudentConfig(admin.ModelAdmin):
    model = User

    list_filter = ('email', 'username', 'major', 'academic_year', 'year_in_school')
    ordering = ('-date_joined',)
    list_display = ('email', 'username', 'major', 'academic_year', 'year_in_school')

    fieldsets = (
        ("Student Information", {'fields': ('email', 'username', 'first_name', 'last_name')}),
        ('Education', {'fields': ('major', 'academic_year', 'year_in_school')}),
    )
# Register your models here.
admin.site.register(User, UserConfig)
admin.site.register(Student, StudentConfig)
