from django.db.models.functions import Coalesce
from django.db.models import Prefetch, Count, Sum, OuterRef, Exists, Subquery, IntegerField, Q, FloatField, Value
from django.db import models

class CourseQuerySet(models.QuerySet):

    def annotate_units_count(self):
        return self.annotate(
        units_count=Count('units', distinct=True),
        )

    def annotate_lectures_count(self):
        return self.annotate(
        lectures_count=Count('units__topics__lectures', distinct=True),
        )

    def annotate_course_duration(self):
        from courses.models import Unit
        course_duration_queryset = Unit.objects.filter(course=OuterRef('pk')).annotate(duration_sum=Sum('topics__lectures__duration')).values('duration_sum')[:1]
        return self.annotate(
        course_duration=Coalesce(Subquery(course_duration_queryset), 0, output_field=FloatField())
        )

    def annotate_is_enrolled(self, user):
        from payment.models import CourseEnrollment
        return self.annotate(
        is_enrolled=Exists(CourseEnrollment.objects.filter(course=OuterRef('pk'), user=user)),
        )


    def annotate_lectures_viewed_count(self, user):
        return self.annotate(
        lectures_viewed_count=Count('activity', filter=Q(activity__user=user, activity__is_finished=True), distinct=True)
        )

    def annotate_all(self, user):
        return self.annotate_units_count().annotate_lectures_count().annotate_course_duration().annotate_is_enrolled(user).annotate_lectures_viewed_count(user)

class CustomCourseManager(models.Manager):
    def get_queryset(self):
        return CourseQuerySet(self.model, using=self._db)

    def annotate_units_count(self):
        return self.get_queryset().annotate_units_count()

    def annotate_lectures_count(self):
        return self.get_queryset().annotate_lectures_count()

    def annotate_course_duration(self):
        return self.get_queryset().annotate_course_duration()

    def annotate_is_enrolled(self):
        return self.get_queryset().annotate_is_enrolled()

    def annotate_lectures_viewed_count(self):
        return self.get_queryset().annotate_lectures_viewed_count()

    def annotate_all(self, user):
        return self.get_queryset().annotate_all(user)
