from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from django.contrib.contenttypes.admin import GenericStackedInline
from .models import Chart, AggregateCard, AggregateFilter, ModelFilter
from django import forms
from django.core.exceptions import ValidationError
from django.urls import path
from django.template.response import TemplateResponse

class AggregateFilterInline(GenericStackedInline):
    model = AggregateFilter
    extra = 1

class ModelFilterInline(GenericStackedInline):
    model = ModelFilter
    extra = 1


class AggregateCardConfig(admin.ModelAdmin):
    model = AggregateCard
    inlines = [AggregateFilterInline, ModelFilterInline]

    def add_view(self, request, form_url='', extra_context=None):
        try:
            return super(AggregateCardConfig, self).add_view(
                request, form_url, extra_context
            )
        except ValidationError as e:
            return handle_exception(self, request, e)

    def get_urls(self):

        # get the default urls
        urls = super(AggregateCardConfig, self).get_urls()

        # define analytics urls
        analytics_urls = [
            path('analytics', self.admin_site.admin_view(self.analytics_configuration), name='analytics')
        ]

        # Make sure here you place your added urls first than the admin default urls
        return analytics_urls + urls

    # Your view definition fn
    def analytics_configuration(self, request):
        # from courses.models import Course
        # from django.db.models import Count
        # course = Course.objects.annotate(Count('enrollments')).filter(enrollments__count__gt=1)
        # print(course)from django.db.models.fields.related import ForeignObjectRel

        charts = Chart.objects.all()
        cards = AggregateCard.objects.select_related('model_type').all()
        data = [2137680, 6282693, 805566, 2568163, 598599, 3189284, 599112, 926340, 5548295, 11847685, 66445];
        labels = ["Management", "Finance", "Human Resources", "Business Development and Marketing", "Information Technology", "Professional Development and Training", "Knowledge Management", "Logistics", "Support", "Business Services", "Other"];

        opts = self.admin_site.get_app_list(request)


        for app in opts:
            if app['app_label'] == 'admin_analytics':
                models = app['models']
                for model in models:
                    if model['object_name'] == 'AggregateCard':
                        current_model = model
                        break
        query = eval('AggregateCard.objects.all()')
        print(query)
        context = dict(
            self.admin_site.each_context(request), # Include common variables for rendering the admin template.
            cards=cards,
            charts=charts,
            data=data,
            labels=labels,
            current_model=current_model
        )
        return TemplateResponse(request, "admin_analytics/base.html", context)


class ChartConfig(admin.ModelAdmin):
    model = Chart
    inlines = [AggregateFilterInline, ModelFilterInline]

admin.site.register(AggregateCard, AggregateCardConfig)
admin.site.register(Chart, ChartConfig)
