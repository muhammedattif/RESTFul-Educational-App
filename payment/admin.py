from django.contrib import admin
from .models import CourseEnrollment
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from import_export.fields import Field
from import_export import resources
from import_export.widgets import DateWidget

class CourseEnrollmentResource(resources.ModelResource):
    date_created = Field(column_name=('Date Created'), attribute='date_created', widget=DateWidget(format='%d.%m.%Y'))
    class Meta:
        model = CourseEnrollment
        widgets = {
                'date_created': {'format': '%d.%m.%Y'},
                }

class CourseEnrollmentConfig(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    model = CourseEnrollment
    resource_class = CourseEnrollmentResource

    list_filter = ('user', 'course', 'payment_method', 'payment_type', 'date_created')
    ordering = ('-date_created',)
    list_display = ('user', 'course', 'payment_method', 'payment_type', 'date_created')
    save_as = True
    save_on_top = True

    fieldsets = (
        ("Course Enrollment Information", {'fields': ('user', 'course', 'payment_method', 'payment_type')}),
    )

admin.site.register(CourseEnrollment, CourseEnrollmentConfig)
