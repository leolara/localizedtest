from django.db import models
from AcademicCatalogueApp.models.course import Course


class Time(models.Model):
    hour = models.CharField(max_length=5)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="times")

    class Meta:
        unique_together = ("hour", "course")

    def __str__(self):
        return self.hour
