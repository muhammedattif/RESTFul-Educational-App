from rest_framework import serializers
from courses.models import Course, Content, CoursePrivacy, ContentPrivacy, Category, Quiz, Question, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = '__all__'

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Quiz
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

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    content = ContentSerializer(many=True, read_only=True)
    privacy = CoursePrivacySerializer(many=False, read_only=True)
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
