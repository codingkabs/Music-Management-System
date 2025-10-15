from django import forms
from django.test import TestCase

from lessons.forms import LogInForm


class TestLogInForm(TestCase):
    def setUp(self):
        self.form_input = {
            "email": "johndoe@example.org",
            "password": "Password123",
        }

    def test_form_has_correct_fields(self):
        form = LogInForm()

        self.assertIn("email", form.fields)
        self.assertIn("password", form.fields)

        password_field = form.fields["password"]

        self.assertTrue(isinstance(password_field.widget, forms.PasswordInput))

    def test_form_accepts_valid_input_data(self):
        self._assert_form_is_valid()

    def test_form_rejects_blank_email(self):
        self.form_input["email"] = ""

        self._assert_form_is_invalid()

    def test_form_rejects_blank_password(self):
        self.form_input["password"] = ""

        self._assert_form_is_invalid()

    def _assert_form_is_valid(self):
        form = LogInForm(self.form_input)

        self.assertTrue(form.is_valid())

    def _assert_form_is_invalid(self):
        form = LogInForm(self.form_input)

        self.assertFalse(form.is_valid())
