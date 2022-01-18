from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from courses.models import Course, CourseActivity, Content, CoursePrivacy, ContentPrivacy, Category, Quiz, QuizResult, Question, Choice, Attachement, Comment, Feedback

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
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ('id', 'question_title', 'choices')

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Quiz
        fields = ('id', 'name', 'description', 'questions')

class QuizResultSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=False, read_only=True)
    selected_choice = ChoiceSerializer(many=False, read_only=True)
    class Meta:
        model = QuizResult
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

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
        fields = ('id', 'title', 'order', 'course', 'privacy', 'viewed')

    def content_viewed(self, content):
        user = self.context.get('request', None).user
        return CourseActivity.objects.filter(content=content, course=content.course, user=user).exists()

class FullContentSerializer(DemoContentSerializer):
    class Meta:
        model = Content
        fields = ('id', 'title', 'video', 'audio', 'text', 'order', 'privacy')

class CourseSerializer(serializers.ModelSerializer):
    number_of_lectures = serializers.SerializerMethodField('get_content_count')
    privacy = CoursePrivacySerializer(many=False, read_only=True)
    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'date_created', 'categories', 'number_of_lectures', 'privacy', 'quiz')
        depth = 1

    def get_content_count(self, course):
        return course.content.count()

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
