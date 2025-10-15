from django import forms

from lessons.models import LessonRequest


class LessonRequestForm(forms.ModelForm):
    class Meta:
        model = LessonRequest
        fields = [
            "is_available_on_monday",
            "is_available_on_tuesday",
            "is_available_on_wednesday",
            "is_available_on_thursday",
            "is_available_on_friday",
            "no_of_lessons",
            "lesson_interval_in_days",
            "lesson_duration_in_mins",
            "further_information",
        ]

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop("current_user", None)
        super(LessonRequestForm, self).__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        no_of_lessons = self.cleaned_data.get("no_of_lessons")
        lesson_interval_in_days = self.cleaned_data.get("lesson_interval_in_days")
        lesson_duration_in_mins = self.cleaned_data.get("lesson_duration_in_mins")

        if no_of_lessons == None or no_of_lessons == 0:
            self.add_error("no_of_lessons", "Cannot be blank or 0.")
        if lesson_interval_in_days == None or lesson_interval_in_days == 0:
            self.add_error("lesson_interval_in_days", "Cannot be blank or 0.")
        if lesson_duration_in_mins == None or lesson_duration_in_mins == 0:
            self.add_error("lesson_duration_in_mins", "Cannot be blank or 0.")

    def save(self, commit=True):
        super().save(commit=False)

        lesson_request = LessonRequest.objects.create(
            is_available_on_monday=self.cleaned_data.get("is_available_on_monday"),
            is_available_on_tuesday=self.cleaned_data.get("is_available_on_tuesday"),
            is_available_on_wednesday=self.cleaned_data.get(
                "is_available_on_wednesday"
            ),
            is_available_on_thursday=self.cleaned_data.get("is_available_on_thursday"),
            is_available_on_friday=self.cleaned_data.get("is_available_on_friday"),
            no_of_lessons=self.cleaned_data.get("no_of_lessons"),
            lesson_interval_in_days=self.cleaned_data.get("lesson_interval_in_days"),
            lesson_duration_in_mins=self.cleaned_data.get("lesson_duration_in_mins"),
            further_information=self.cleaned_data.get("further_information"),
            user=self.current_user,
        )

        return lesson_request
