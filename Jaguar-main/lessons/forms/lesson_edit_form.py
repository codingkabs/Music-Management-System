from django import forms

from lessons.models import Lesson


class LessonEditForm(forms.ModelForm):

    class Meta:
        model = Lesson
        fields = ("datetime", "teacher", "duration", "further_information")
        widgets = {
            "datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "duration": forms.NumberInput(attrs={"placeholder": "e.g. 45 minutes"})
        }