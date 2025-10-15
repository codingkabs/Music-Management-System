from django import forms
from django.test import TestCase
from django.contrib.auth.hashers import check_password

from lessons.forms import SignUpForm
from lessons.models import User


class TestSignUpForm(TestCase):
    def setUp(self):
        self.form_input = {
            "email": "johndoe@example.org",
            "first_name": "John",
            "last_name": "Doe",
            "new_password": "Password123",
            "password_confirmation": "Password123",
        }

    def test_valid_sign_up_form(self):
        form = SignUpForm(data=self.form_input)

        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = SignUpForm()

        self.assertIn("first_name", form.fields)
        self.assertIn("last_name", form.fields)

        self.assertIn("email", form.fields)
        email_field = form.fields["email"]
        self.assertTrue(isinstance(email_field, forms.EmailField))

        self.assertIn("new_password", form.fields)
        new_password_widget = form.fields["new_password"].widget
        self.assertTrue(isinstance(new_password_widget, forms.PasswordInput))

        self.assertIn("password_confirmation", form.fields)
        password_confirmation_widget = form.fields["password_confirmation"].widget
        self.assertTrue(isinstance(password_confirmation_widget, forms.PasswordInput))

    def test_form_uses_model_validation(self):
        self.form_input["email"] = "bademail"

        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_and_password_confirmation_are_identical(self):
        self.form_input["password_confirmation"] = "WrongPassword123"

        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        before_user_count = User.objects.count()

        form = SignUpForm(data=self.form_input)
        form.save()

        after_user_count = User.objects.count()

        self.assertEqual(after_user_count, before_user_count + 1)

        user = User.objects.get(email="johndoe@example.org")

        is_password_correct = check_password("Password123", user.password)

        self.assertTrue(is_password_correct)

    def test_form_creates_student_user(self):
        form = SignUpForm(data=self.form_input)
        form.save()

        user = User.objects.get(email="johndoe@example.org")

        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.role, "Student")
