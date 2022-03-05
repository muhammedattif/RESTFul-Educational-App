from django.contrib import admin
from django.db import transaction
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from courses.models import (
Course, CoursePrivacy,
CourseAttachement,
ContentAttachement,
Content, ContentPrivacy,
CourseActivity,
Comment,
Feedback,
CorrectInfo,
Report,
Feedback,
Quiz,
Question,
Choice,
QuizResult,
QuizAttempt,
Unit,
Topic
)

admin.site.register(QuizResult)
admin.site.register(QuizAttempt)
admin.site.register(Unit)
class UnitTopicsInline(NestedStackedInline):
    model = Topic
    can_delete = True
    extra = 1
    verbose_name_plural = 'Topics'
    fk_name = 'unit'

class CourseUnitsInline(NestedStackedInline):
    model = Unit
    can_delete = False
    extra = 2
    verbose_name_plural = 'Units'
    fk_name = 'course'
    inlines = [UnitTopicsInline]

class CoursePrivacyInline(NestedStackedInline):
    model = CoursePrivacy
    can_delete = False
    verbose_name_plural = 'Privacy'
    fk_name = 'course'


class CourseAttachementsInline(NestedStackedInline):
    model = CourseAttachement
    can_delete = True
    verbose_name_plural = 'Attachements'
    fk_name = 'course'

class CourseConfig(NestedModelAdmin):
    model = Course

    list_filter = ('categories', 'date_created')
    ordering = ('-date_created',)
    list_display = ('title', 'date_created')

    fieldsets = (
        ("Course Information", {'fields': ('image', 'title', 'description', 'price', 'categories', 'tags', 'featured', 'quiz')}),
    )

    @transaction.atomic
    def save_formset(self, request, form, formset, change):
        try:
            super().save_formset(request, form, formset, change)
        except Exception as e:
            print(e)
            pass

    inlines = [CoursePrivacyInline, CourseAttachementsInline, CourseUnitsInline]


admin.site.register(Course, CourseConfig)

###### Course Content
class ContentAttachementsInline(NestedStackedInline):
    model = ContentAttachement
    can_delete = True
    verbose_name_plural = 'Attachements'
    fk_name = 'content'

class ContentPrivacyInline(NestedStackedInline):
    model = ContentPrivacy
    can_delete = False
    verbose_name_plural = 'Privacy'
    fk_name = 'content'

class ContentConfig(NestedModelAdmin):
    model = Content

    list_filter = ('topic', )
    list_display = ('topic', 'title')

    fieldsets = (
        ("Content Information", {'fields': ('title', 'description', 'topic', 'video', 'audio', 'text', 'duration', 'order', 'quiz')}),
    )

    inlines = [ContentPrivacyInline, ContentAttachementsInline]

admin.site.register(Content, ContentConfig)
admin.site.register(CourseActivity)

class CommentConfig(NestedModelAdmin):
    model = Comment

    list_filter = ('user', 'object_type', 'date_created', 'status')
    list_display = ('user', 'object_type', 'date_created', 'status')

    fieldsets = (
        ("Comment Information", {'fields': ('user', 'object_type', 'object_id', 'comment_body', 'status')}),
    )

admin.site.register(Comment, CommentConfig)

class FeedbackConfig(NestedModelAdmin):
    model = Feedback

    list_filter = ('user', 'course', 'rating' ,'date_created')
    list_display = ('user', 'course', 'rating', 'date_created')

    fieldsets = (
        ("Feedback Information", {'fields': ('user', 'course', 'rating', 'description')}),
    )
admin.site.register(Feedback, FeedbackConfig)
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
