from django.db import models
from django.core.validators import MinValueValidator

from lessons.models import User

# Create the class for LessonRequest for the days in the week
# default set to true

class LessonRequest(models.Model):
    is_available_on_monday = models.BooleanField(null=True,
                                                 blank=True,
                                                 default=True)
    is_available_on_tuesday = models.BooleanField(null=True,
                                                  blank=True,
                                                  default=True)
    is_available_on_wednesday = models.BooleanField(null=True,
                                                    blank=True,
                                                    default=True)
    is_available_on_thursday = models.BooleanField(null=True,
                                                   blank=True,
                                                   default=True)
    is_available_on_friday = models.BooleanField(null=True,
                                                 blank=True,
                                                 default=True)

    no_of_lessons = models.IntegerField(validators=[MinValueValidator(1)])
    lesson_interval_in_days = models.IntegerField(
        validators=[MinValueValidator(1)])
    lesson_duration_in_mins = models.IntegerField(
        validators=[MinValueValidator(1)])
    # additional information section, allows users to keep empty if not needed.
    further_information = models.CharField(max_length=255,
                                           null=True,
                                           blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    is_fulfilled = models.BooleanField(default=False)
