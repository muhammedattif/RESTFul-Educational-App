from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, Student, Teacher
from django.contrib.auth.forms import (
    AdminPasswordChangeForm
)

class UserConfig(UserAdmin):
    model = User
    change_password_form = AdminPasswordChangeForm

    list_filter = ('email', 'username', 'is_active', 'is_staff')
    ordering = ('-date_joined',)
    list_display = ('email', 'username',
                    'is_active', 'is_staff')

    fieldsets = (
        ("User Information", {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_student', 'is_teacher', 'is_superuser', 'groups', 'user_permissions')}),
    )

class StudentConfig(admin.ModelAdmin):
    model = Student

    list_filter = ('user', 'major', 'academic_year', 'year_in_school')
    list_display = ('user', 'major', 'academic_year', 'year_in_school')

    fieldsets = (
        ("Student Account", {'fields': ('user', )}),
        ('Education', {'fields': ('major', 'academic_year', 'year_in_school')}),
    )

class TeacherConfig(admin.ModelAdmin):
    model = Teacher

    list_filter = ('major', )
    list_display = ('user', 'major')


# Register your models here.
admin.site.register(User, UserConfig)
admin.site.register(Student, StudentConfig)
admin.site.register(Teacher, TeacherConfig)
