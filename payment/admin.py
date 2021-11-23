from django.contrib import admin
from .models import CourseEnrollment

class CourseEnrollmentConfig(admin.ModelAdmin):
    model = CourseEnrollment

    list_filter = ('user', 'course', 'payment_method', 'payment_type', 'date_created')
    ordering = ('-date_created',)
    list_display = ('user', 'course', 'payment_method', 'payment_type', 'date_created')

    fieldsets = (
        ("Course Enrollment Information", {'fields': ('user', 'course', 'payment_method', 'payment_type')}),
    )

admin.site.register(CourseEnrollment, CourseEnrollmentConfig)
