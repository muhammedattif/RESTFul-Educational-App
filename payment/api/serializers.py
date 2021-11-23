from rest_framework import serializers
from payment.models import CourseEnrollment

class CourseEnrollmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseEnrollment
        fields = '__all__'
