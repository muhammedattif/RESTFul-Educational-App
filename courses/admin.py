from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from courses.models import (
Course, CoursePrivacy,
Category, Attachement,
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

    inlines = [CoursePrivacyInline, AttachementsInline]


admin.site.register(Course, CourseConfig)
admin.site.register(Category)

###### Course Content

class ContentPrivacyInline(admin.StackedInline):
    model = ContentPrivacy
    can_delete = False
    verbose_name_plural = 'Privacy'
    fk_name = 'content'

class ContentConfig(admin.ModelAdmin):
    model = Content

    list_filter = ('course', )
    list_display = ('course', 'title')

    fieldsets = (
        ("Content Information", {'fields': ('title', 'course', 'video_content', 'audio_content', 'text_content', 'order', 'quiz')}),
    )

    inlines = (ContentPrivacyInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(ContentConfig, self).get_inline_instances(request, obj)

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
