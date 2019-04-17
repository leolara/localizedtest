from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)
    professor = models.CharField(max_length=200, null=False, blank=False)
    cost = models.IntegerField()

    def __str__(self):
        return self.name + " "
