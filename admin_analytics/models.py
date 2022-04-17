from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldError
from django.db.models.fields.related import ForeignObjectRel
import ast

class AggrigateFunctions(models.TextChoices):
    COUNT = ("count", 'Count')
    SUM = ("sum", 'Sum')
    MIN = ("min", 'Min')
    MAX = ("max", 'Max')
    AVG = ("avg", 'Avg')

class ChartTypes(models.TextChoices):
    PIE = ("pie", 'Pie')
    LINE = ("line", 'Line')
    AREA = ("area", 'Area')
    BAR = ("bar", 'Bar')
    SCATTER = ("scatter", 'Scatter')
    POLAR = ("polar", 'Polar')
    BUBBLE = ("bubble", 'Bubble')
    DOUGHNUT = ("doughnut", 'Doughnut')


class AggrigateFunctionsMapper:

    AGGREGATE_SYMBOLS = {
        AggrigateFunctions.COUNT: models.Count,
        AggrigateFunctions.SUM: models.Sum,
        AggrigateFunctions.MIN: models.Min,
        AggrigateFunctions.MAX: models.Max,
        AggrigateFunctions.AVG: models.Avg,
    }

    @classmethod
    def get_aggregate_function(self, aggrigate_function):
        return self.AGGREGATE_SYMBOLS[aggrigate_function]

class AggregateFilter(models.Model):

    choices = models.Q(app_label = 'admin_analytics', model = 'Card') | models.Q(app_label = 'admin_analytics', model = 'Chart')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=choices, related_name='aggregate_filters')
    object_id = models.PositiveIntegerField()
    config_object = GenericForeignKey(ct_field='content_type',
                                      fk_field='object_id')

    field = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        repr = self.field[0:self.field.index("__")] if '__' in self.field else self.field
        return f'{repr} Filter'


class ModelFilter(models.Model):

    choices = models.Q(app_label = 'admin_analytics', model = 'Card') | models.Q(app_label = 'admin_analytics', model = 'Chart')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=choices, related_name='model_filters')
    object_id = models.PositiveIntegerField()
    config_object = GenericForeignKey(ct_field='content_type',
                                      fk_field='object_id')

    field = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        repr = self.field[0:self.field.index("__")] if '__' in self.field else self.field
        return f'{repr} Filter'

class AggregateCard(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    model_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    aggrigate_function = models.CharField(max_length=100, choices=AggrigateFunctions.choices)
    aggregate_field = models.CharField(blank=True, max_length=100, default='pk')

    def __str__(self):
        return self.name

    def execute(self):
        try:
            aggregate_function = AggrigateFunctionsMapper.get_aggregate_function(self.aggrigate_function)
            model = self.model_type.model_class()


            related_fields = [field.get_accessor_name() for field in model._meta.get_fields() if issubclass(type(field), ForeignObjectRel)]


            model_filters = dict()
            for filter in self.model_filters.values('field', 'value'):
                try:
                    evaluated_value = ast.literal_eval(filter['value'])
                except ValueError:
                    evaluated_value =  filter['value']
                model_filters[filter['field']] = evaluated_value


            aggregate_filters = dict()
            for filter in self.aggregate_filters.values('field', 'value'):
                try:
                    evaluated_value = ast.literal_eval(filter['value'])
                except ValueError:
                    evaluated_value =  filter['value']
                aggregate_filters[filter['field']] = evaluated_value

            queryset = model.objects.filter(**model_filters)
            if self.aggrigate_function == AggrigateFunctions.COUNT:
                queryset = queryset.annotate(aggregate_function(self.aggregate_field)).filter(**aggregate_filters).count()
            else:
                queryset = queryset.aggregate(aggregate_function(self.aggregate_field))
                queryset = queryset[f'{self.aggregate_field}__{self.aggrigate_function}']
            return round(queryset,2)
        except FieldError as e:
            print(e)
            return f"Cannot resolve one of filter keywords into field."

    @property
    def model_filters(self):
        return ModelFilter.objects.filter(content_type=ContentType.objects.get_for_model(self).id, object_id=self.id)

    @property
    def aggregate_filters(self):
        return AggregateFilter.objects.filter(content_type=ContentType.objects.get_for_model(self).id, object_id=self.id)

class Chart(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    model_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    aggrigate_function = models.CharField(max_length=100, choices=AggrigateFunctions.choices)
    aggregate_field = models.CharField(blank=True, max_length=100, default='pk')
    order_by = models.CharField(blank=True, max_length=100, default='pk', help_text="Default is pk.")
    type = models.CharField(max_length=100, choices=ChartTypes.choices)

    def __str__(self):
        return self.name

    def execute(self):
        aggregate_function = AggrigateFunctionsMapper.get_aggregate_function(self.aggrigate_function)
        model = self.model_type.model_class()

        model_filters = dict()
        for filter in self.model_filters.values('field', 'value'):
            try:
                evaluated_value = ast.literal_eval(filter['value'])
            except ValueError:
                evaluated_value =  filter['value']
            model_filters[filter['field']] = evaluated_value


        aggregate_filters = dict()
        for filter in self.aggregate_filters.values('field', 'value'):
            try:
                evaluated_value = ast.literal_eval(filter['value'])
            except ValueError:
                evaluated_value =  filter['value']
            aggregate_filters[filter['field']] = evaluated_value

        queryset = model.objects.filter(**model_filters)
        queryset = queryset.annotate(value=aggregate_function(self.aggregate_field), label=models.F(self.label)).filter(**aggregate_filters).order_by(self.order_by)
        queryset = queryset.values('id','label', 'value')
        return queryset

    @property
    def model_filters(self):
        return ModelFilter.objects.filter(content_type=ContentType.objects.get_for_model(self).id, object_id=self.id)

    @property
    def aggregate_filters(self):
        return AggregateFilter.objects.filter(content_type=ContentType.objects.get_for_model(self).id, object_id=self.id)
