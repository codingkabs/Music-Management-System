from django.test import TestCase
from django.urls import reverse
from django.contrib import messages

from lessons.forms import LogInForm
from lessons.models import User
from lessons.tests.helpers import Helper


class LogInViewTestCase(TestCase, Helper):

    def setUp(self):
        self.url = reverse("log_in")

        self.user = User.objects.create_user(email="johndoe@example.org", password="Password123")

    def test_log_in_url(self):
        self.assertEqual(self.url, "/login/")

    def test_get_log_in(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "log_in.html")

        form = response.context["form"]

        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)

        messages_list = list(response.context["messages"])

        self.assertEqual(len(messages_list), 0)

    def test_unsuccessful_log_in(self):
        form_input = {"email": "johndoe@example.org", "password": "WrongPassword123"}

        response = self.client.post(self.url, form_input)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "log_in.html")

        form = response.context["form"]

        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())

        messages_list = list(response.context["messages"])

        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_log_in_with_blank_username(self):
        form_input = {"email": "", "password": "Password123"}

        response = self.client.post(self.url, form_input)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "log_in.html")

        form = response.context["form"]

        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())

        messages_list = list(response.context["messages"])

        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_log_in_with_blank_password(self):
        form_input = {"email": "johndoe@example.org", "password": ""}

        response = self.client.post(self.url, form_input)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "log_in.html")

        form = response.context["form"]

        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())

        messages_list = list(response.context["messages"])

        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_successful_log_in(self):
        form_input = {"email": "johndoe@example.org", "password": "Password123"}

        response = self.client.post(self.url, form_input, follow=True)

        self.assertTrue(self._is_logged_in())

        response_url = reverse("student/lesson-requests")

        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "student/lesson_requests.html")

        messages_list = list(response.context["messages"])

        self.assertEqual(len(messages_list), 0)

    def test_valid_log_in_by_inactive_user(self):
        self.user.is_active = False
        self.user.save()

        form_input = {"email": "johndoe@example.org", "password": "Password123"}

        response = self.client.post(self.url, form_input, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "log_in.html")

        form = response.context["form"]

        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())

        messages_list = list(response.context["messages"])

        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
