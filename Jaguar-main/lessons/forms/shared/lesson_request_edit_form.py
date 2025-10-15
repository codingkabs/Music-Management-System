from django import forms

from lessons.models import LessonRequest


class LessonRequestEditForm(forms.ModelForm):

    class Meta:
        model = LessonRequest
        fields = ("no_of_lessons", "lesson_duration_in_mins", "lesson_interval_in_days", "further_information")
