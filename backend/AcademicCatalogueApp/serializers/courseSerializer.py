from rest_framework import serializers
from ..models import Course

# This is necessary to include times when retrieving the courses
class CourseSerializer(serializers.ModelSerializer):
    times = serializers.SlugRelatedField(many=True, read_only=True, slug_field="hour")

    class Meta:
        fields = "__all__"
        model = Course
