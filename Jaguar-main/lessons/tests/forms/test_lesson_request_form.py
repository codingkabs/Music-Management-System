from django import forms
from django.test import TestCase

from lessons.forms import LessonRequestForm


class TestLessonRequestForm(TestCase):
    def setUp(self):
        self.form_input = {
            "is_available_on_monday": True,
            "is_available_on_tuesday": False,
            "is_available_on_wednesday": False,
            "is_available_on_thursday": False,
            "is_available_on_friday": True,
            "no_of_lessons": 3,
            "lesson_interval_in_days": 7,
            "lesson_duration_in_mins": 30,
            "further_information": "I prefer teacher X.",
        }

    def test_form_has_correct_fields(self):
        form = LessonRequestForm()

        self.assertIn("is_available_on_monday", form.fields)
        self.assertIn("is_available_on_tuesday", form.fields)
        self.assertIn("is_available_on_wednesday", form.fields)
        self.assertIn("is_available_on_thursday", form.fields)
        self.assertIn("is_available_on_friday", form.fields)
        self.assertIn("no_of_lessons", form.fields)
        self.assertIn("lesson_interval_in_days", form.fields)
        self.assertIn("lesson_duration_in_mins", form.fields)
        self.assertIn("further_information", form.fields)

    def test_form_accepts_valid_input_data(self):
        self._assert_form_is_valid()

    def test_form_rejects_no_of_lessons_as_zero(self):
        self.form_input["no_of_lessons"] = 0

        self._assert_form_is_invalid()

    def test_form_rejects_lesson_interval_in_days_as_zero(self):
        self.form_input["lesson_interval_in_days"] = 0

        self._assert_form_is_invalid()

    def test_form_rejects_lesson_duration_in_mins_as_zero(self):
        self.form_input["lesson_duration_in_mins"] = 0

        self._assert_form_is_invalid()

    def _assert_form_is_valid(self):
        form = LessonRequestForm(self.form_input)

        self.assertTrue(form.is_valid())

    def _assert_form_is_invalid(self):
        form = LessonRequestForm(self.form_input)

        self.assertFalse(form.is_valid())
