from rest_framework import serializers
from courses.models import Course, Content, CoursePrivacy, ContentPrivacy, Category, Quiz, Question, Choice, Attachement, Comment, Feedback

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

class DemoContentSerializer(serializers.ModelSerializer):
    privacy = ContentPrivacySerializer(many=False, read_only=True)
    class Meta:
        model = Content
        fields = ('id', 'title', 'order', 'course', 'privacy')

class FullContentSerializer(DemoContentSerializer):
    class Meta:
        model = Content
        fields = ('id', 'title', 'video_content', 'audio_content', 'text_content', 'order', 'privacy')

class CourseSerializer(serializers.ModelSerializer):
    privacy = CoursePrivacySerializer(many=False, read_only=True)
    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'date_created', 'categories', 'privacy', 'quiz')
        depth = 1

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
