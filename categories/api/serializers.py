from rest_framework import serializers
from categories.models import Category

class CategorySerializer(serializers.ModelSerializer):
    number_of_courses = serializers.SerializerMethodField('get_number_of_courses')
    class Meta:
        model = Category
        fields = '__all__'

    def get_number_of_courses(self, category):
        return category.course_set.count()
