from django.db import models

from lessons.models import User, Teacher, LessonRequest

# Create the class for Lessons, giving the specific attributes and their datafield

class Lesson(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    datetime = models.DateTimeField()

    duration = models.IntegerField()

    further_information = models.CharField(max_length=255,
                                           null=True,
                                           blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    lesson_request = models.ForeignKey(LessonRequest, on_delete=models.CASCADE)
