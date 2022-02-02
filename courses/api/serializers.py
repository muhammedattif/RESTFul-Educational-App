from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from courses.models import Course, CourseActivity, Content, CoursePrivacy, ContentPrivacy, Category, Quiz, QuizResult, Question, Choice, Attachement, Comment, Feedback
from categories.api.serializers import CategorySerializer
from django.db.models import Sum
from payment.models import CourseEnrollment


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

class AttachementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachement
        fields = '__all__'

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'choice', 'is_correct')

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ('id', 'question_title', 'choices')

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    # number_of_questions = serializers.CharField(source='get_questions_count')
    class Meta:
        model = Quiz
        fields = ('id', 'name', 'description', 'questions')

class BaseQuizResultSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=False, read_only=True)
    selected_choice = ChoiceSerializer(many=False, read_only=True)
    class Meta:
        model = QuizResult
        fields = ('id', 'question', 'selected_choice', 'is_correct')

class QuizResultSerializer(serializers.ModelSerializer):
    selected_choice = ChoiceSerializer(many=False, read_only=True)
    result = serializers.SerializerMethodField('get_result')
    questions_count = serializers.SerializerMethodField('get_questions_count')
    score = serializers.SerializerMethodField('get_score')
    class Meta:
        model = Quiz
        fields = '__all__'

    num_of_right_answers = 0
    def get_result(self, quiz):
        user = self.context.get('request', None).user
        # Must select distinct, but it is not supported by SQLite
        quiz_answers = QuizResult.objects.select_related('question', 'selected_choice').prefetch_related('question__choices').filter(user=user, quiz=quiz)
        self.num_of_right_answers = quiz_answers.filter(is_correct=True).count()
        return BaseQuizResultSerializer(quiz_answers, many=True, read_only=True).data

    def get_score(self, quiz):
        return self.num_of_right_answers


    def get_questions_count(self, quiz):
        return quiz.questions.count()

class CoursePrivacySerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursePrivacy
        fields = '__all__'

class ContentPrivacySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentPrivacy
        fields = '__all__'

class CourseActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseActivity
        fields = '__all__'

class DemoContentSerializer(serializers.ModelSerializer):
    viewed = serializers.SerializerMethodField('content_viewed')
    privacy = ContentPrivacySerializer(many=False, read_only=True)
    class Meta:
        model = Content
        fields = ('id', 'title', 'order', 'course', 'privacy', 'viewed', 'duration')

    def content_viewed(self, content):
        user = self.context.get('request', None).user
        return content.activity.filter(user=user).exists()

class FullContentSerializer(DemoContentSerializer):
    class Meta:
        model = Content
        fields = ('id', 'course_id', 'title', 'video', 'audio', 'text', 'duration', 'order', 'privacy')

    def get_course_id(self, content):
        return content.course.id

class QuerySerializerMixin(object):
    PREFETCH_FIELDS = [] # Here is for M2M fields
    RELATED_FIELDS = [] # Here is for ForeignKeys

    @classmethod
    def get_related_queries(cls, queryset):
        # This method we will use in our ViewSet
        # for modify queryset, based on RELATED_FIELDS and PREFETCH_FIELDS
        if cls.RELATED_FIELDS:
            queryset = queryset.select_related(*cls.RELATED_FIELDS)
        if cls.PREFETCH_FIELDS:
            queryset = queryset.prefetch_related(*cls.PREFETCH_FIELDS)
        return queryset

class CourseSerializer(serializers.ModelSerializer, QuerySerializerMixin):
    progress = serializers.SerializerMethodField('get_progress')
    duration = serializers.SerializerMethodField('get_duration')
    is_enrolled = serializers.SerializerMethodField('get_enrollment')
    number_of_lectures = serializers.IntegerField(source='get_content_count')
    privacy = CoursePrivacySerializer(many=False, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    PREFETCH_FIELDS = ['content', 'categories__course_set', 'privacy__shared_with']


    class Meta:
        model = Course
        fields = ('id', 'image', 'title', 'description', 'date_created', 'categories', 'price', 'privacy', 'quiz', 'number_of_lectures', 'duration', 'progress', 'is_enrolled')

    def get_progress(self, course):
        user = self.context.get('request', None).user
        content_viewed_count = course.activity.filter(user=user).count()

        content_count = course.get_content_count()
        if not content_count:
            return 0.0
        return content_viewed_count/content_count*100

    def get_duration(self, course):
        duration = course.content.aggregate(sum=Sum('duration'))['sum']
        return duration

    def get_enrollment(self, course):
        user = self.context.get('request', None).user
        return CourseEnrollment.objects.filter(user=user, course=course).exists()



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
