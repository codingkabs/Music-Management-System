from datetime import datetime

from django import forms
from django.test import TestCase

from lessons.forms import LessonEditForm
from lessons.models import Teacher


class TestLessonEditForm(TestCase):

    def setUp(self):
        self.teacher = Teacher.objects.create(first_name="John", last_name="Doe")
        self.form_input = {
            "datetime": datetime.now(),
            "teacher": self.teacher,
            "duration": 45,
            "further_information": "Hello, world!",
        }

    def test_form_has_correct_fields(self):
        form = LessonEditForm()

        self.assertIn("datetime", form.fields)
        self.assertIn("teacher", form.fields)
        self.assertIn("duration", form.fields)
        self.assertIn("further_information", form.fields)

        datetime_field = form.fields["datetime"]

        self.assertTrue(isinstance(datetime_field.widget, forms.DateTimeInput))

    def test_form_accepts_valid_input_data(self):
        self._assert_form_is_valid()

    def _assert_form_is_valid(self):
        form = LessonEditForm(self.form_input)

        self.assertTrue(form.is_valid())

    def _assert_form_is_invalid(self):
        form = LessonEditForm(self.form_input)

        self.assertFalse(form.is_valid())
