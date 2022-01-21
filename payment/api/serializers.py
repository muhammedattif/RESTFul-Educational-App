from rest_framework import serializers
from payment.models import CourseEnrollment

class CourseEnrollmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseEnrollment
        fields = '__all__'

    def create(self, validated_data):
        course_enrollment, created = CourseEnrollment.objects.get_or_create(**validated_data)
        return course_enrollment
