from django import forms

from lessons.models import Lesson


class LessonCreateForm(forms.ModelForm):

    class Meta:
        model = Lesson
        fields = ("datetime", "teacher", "duration", "further_information", "user", "lesson_request")
        widgets = {
            "datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "user": forms.HiddenInput(),
            "lesson_request": forms.HiddenInput(),
            "duration": forms.NumberInput(attrs={"placeholder": "e.g. 45 minutes"})
        }