from django.contrib import admin
from django.db import transaction
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from courses.models import (
Course, CoursePrivacy,
Attachement,
Content, ContentPrivacy,
CourseProgress,
Comment,
Feedback,
CorrectInfo,
Report,
Quiz,
Question,
Choice
)

class CoursePrivacyInline(NestedStackedInline):
    model = CoursePrivacy
    can_delete = False
    verbose_name_plural = 'Privacy'
    fk_name = 'course'


class AttachementsInline(NestedStackedInline):
    model = Attachement
    can_delete = True
    verbose_name_plural = 'Attachements'
    fk_name = 'course'

class CourseConfig(NestedModelAdmin):
    model = Course

    list_filter = ('categories', 'date_created')
    ordering = ('-date_created',)
    list_display = ('title', 'date_created')

    fieldsets = (
        ("Course Information", {'fields': ('title', 'description', 'categories', 'quiz')}),
    )

    @transaction.atomic
    def save_formset(self, request, form, formset, change):
        try:
            super().save_formset(request, form, formset, change)
        except Exception as e:
            print(e)
            pass

    inlines = [CoursePrivacyInline, AttachementsInline]


admin.site.register(Course, CourseConfig)

###### Course Content

class ContentPrivacyInline(NestedStackedInline):
    model = ContentPrivacy
    can_delete = False
    verbose_name_plural = 'Privacy'
    fk_name = 'content'

class ContentConfig(NestedModelAdmin):
    model = Content

    list_filter = ('course', )
    list_display = ('course', 'title')

    fieldsets = (
        ("Content Information", {'fields': ('title', 'course', 'video_content', 'audio_content', 'text_content', 'order', 'quiz')}),
    )

    inlines = [ContentPrivacyInline]

admin.site.register(Content, ContentConfig)
admin.site.register(CourseProgress)

admin.site.register(Comment)
admin.site.register(Feedback)


admin.site.register(CorrectInfo)
admin.site.register(Report)



class ChoiceInline(NestedStackedInline):
    model = Choice
    can_delete = True
    verbose_name_plural = 'Choices'
    fk_name = 'question'


class QuestionInline(NestedStackedInline):
    model = Question
    extra = 1
    can_delete = True
    verbose_name_plural = 'Questions'
    fk_name = 'quiz'
    inlines = [ChoiceInline]


class QuizConfig(NestedModelAdmin):
    model = Quiz
    inlines = [QuestionInline]

admin.site.register(Quiz, QuizConfig)


# models order
