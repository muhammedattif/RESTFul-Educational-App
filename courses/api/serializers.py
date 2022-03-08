from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from courses.models import (
Course, Unit, Topic,
CourseActivity,
Lecture, CoursePrivacy,
LecturePrivacy, Category,
Quiz, QuizResult, Question, Choice,
Attachement, Comment, Feedback
)
from alteby.utils import seconds_to_duration
from categories.api.serializers import CategorySerializer, TagSerializer
from django.db.models import Sum
from payment.models import CourseEnrollment
from alteby.utils import seconds_to_duration


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

class LecturePrivacySerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturePrivacy
        fields = '__all__'

class CourseActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseActivity
        fields = '__all__'

class DemoLectureSerializer(serializers.ModelSerializer):
    viewed = serializers.BooleanField()
    privacy = LecturePrivacySerializer(many=False, read_only=True)
    class Meta:
        model = Lecture
        fields = ('id', 'title', 'order', 'topic', 'privacy', 'viewed', 'duration')

    def is_viewed(self, lecture):
        user = self.context.get('request', None).user
        return lecture.activity.filter(user=user).exists()

class FullLectureSerializer(DemoLectureSerializer):
    duration = serializers.SerializerMethodField('convert_duration')
    class Meta:
        model = Lecture
        fields = ('id', 'topic_id', 'title', 'video', 'audio', 'text', 'duration', 'order', 'privacy')

    def convert_duration(self, lecture):
        return seconds_to_duration(lecture.duration)

    def get_course_id(self, lecture):
        return lecture.course.id

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

class TopicsListSerializer(serializers.ModelSerializer):
    lectures_count = serializers.IntegerField()
    lectures_duration = serializers.SerializerMethodField('format_lectures_duration')
    is_finished = serializers.SerializerMethodField('get_activity_status')

    class Meta:
        model = Topic
        fields =('id', 'title', 'unit', 'lectures_count', 'lectures_duration', 'is_finished', 'order')

    def get_activity_status(self, topic):
        return topic.lectures_count == topic.num_of_lectures_viewed

    def format_lectures_duration(self, topic):
        return seconds_to_duration(topic.lectures_duration)


class TopicDetailSerializer(serializers.ModelSerializer):
    lectures_count = serializers.IntegerField()
    lectures_duration = serializers.SerializerMethodField('format_lectures_duration')
    is_finished = serializers.SerializerMethodField('get_activity_status')

    class Meta:
        model = Topic
        fields =('id', 'title', 'unit', 'lectures_count', 'lectures_duration', 'is_finished', 'order')

    def get_activity_status(self, unit):
        return unit.lectures_count == unit.num_of_lectures_viewed

    def format_lectures_duration(self, unit):
        return seconds_to_duration(unit.lectures_duration)

class UnitSerializer(serializers.ModelSerializer):
    lectures_count = serializers.IntegerField()
    lectures_duration = serializers.SerializerMethodField('format_lectures_duration')
    is_finished = serializers.SerializerMethodField('get_activity_status')

    class Meta:
        model = Unit
        fields = ('id', 'title', 'course', 'order', 'lectures_duration', 'lectures_count', 'is_finished')

    def get_activity_status(self, unit):
        return unit.lectures_count == unit.num_of_lectures_viewed

    def format_lectures_duration(self, unit):
        return seconds_to_duration(unit.lectures_duration)

class UnitTopicsSerializer(serializers.ModelSerializer):
    topics = TopicsListSerializer(many=True, read_only=True)
    lectures_count = serializers.IntegerField(source='get_lectures_count')
    lectures_duration = serializers.CharField(source='get_lectures_duration')
    class Meta:
        model = Unit
        fields = ('id', 'title', 'course', 'order', 'topics', 'lectures_duration', 'lectures_count')

class CourseSerializer(serializers.ModelSerializer, QuerySerializerMixin):
    progress = serializers.SerializerMethodField('get_progress')
    is_enrolled = serializers.BooleanField()
    units_count = serializers.IntegerField()
    lectures_count = serializers.IntegerField()

    # Flag: this field hits the DB
    is_finished = serializers.SerializerMethodField('get_activity_status')

    duration = serializers.SerializerMethodField('format_lectures_duration')
    privacy = CoursePrivacySerializer(many=False, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    PREFETCH_FIELDS = ['categories__course_set', 'privacy__shared_with']


    class Meta:
        model = Course
        fields = (
        'id', 'image', 'title',
        'description', 'date_created',
        'categories', 'tags', 'price',
        'privacy', 'quiz',
        'units_count', 'lectures_count', 'duration', 'progress', 'is_enrolled', 'is_finished')

    def get_progress(self, course):
        user = self.context.get('request', None).user
        lectures_viewed_count = course.lectures_viewed_count

        lectures_count = course.lectures_count
        if not lectures_count:
            return 0.0
        return lectures_viewed_count/lectures_count*100


    def get_enrollment(self, course):
        user = self.context.get('request', None).user
        return CourseEnrollment.objects.filter(user=user, course=course).exists()

    def get_activity_status(self, course):
        return course.lectures_count == course.lectures_viewed_count

    def format_lectures_duration(self, course):
        return seconds_to_duration(course.duration)


class CoursesSerializer(serializers.ModelSerializer, QuerySerializerMixin):
    progress = serializers.SerializerMethodField('get_progress')
    is_enrolled = serializers.BooleanField()
    units_count = serializers.IntegerField()
    lectures_count = serializers.IntegerField()

    # Flag: this field hits the DB
    is_finished = serializers.SerializerMethodField('get_activity_status')

    duration = serializers.SerializerMethodField('format_lectures_duration')
    privacy = CoursePrivacySerializer(many=False, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    PREFETCH_FIELDS = ['categories__course_set', 'privacy__shared_with']


    class Meta:
        model = Course
        fields = (
        'id', 'image', 'title',
        'description', 'date_created',
        'categories', 'tags', 'price',
        'privacy', 'quiz',
        'units_count', 'lectures_count', 'duration', 'progress', 'is_enrolled', 'is_finished')

    def get_progress(self, course):
        lectures_viewed_count = course.lectures_viewed_count

        lectures_count = course.lectures_count
        if not lectures_count:
            return 0.0
        return lectures_viewed_count/lectures_count*100


    def get_enrollment(self, course):
        user = self.context.get('request', None).user
        return CourseEnrollment.objects.filter(user=user, course=course).exists()

    def get_activity_status(self, course):
        return course.lectures_count == course.lectures_viewed_count

    def format_lectures_duration(self, course):
        return seconds_to_duration(course.duration)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
