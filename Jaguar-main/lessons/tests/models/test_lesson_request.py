# test further information can be empty string

from django.core.exceptions import ValidationError
from django.test import TestCase

from lessons.models import LessonRequest, User


class TestLessonRequest(TestCase):
    fixtures_path = "lessons/tests/fixtures"
    fixtures = [f"{fixtures_path}/user_john.json", f"{fixtures_path}/lesson_request.json"]

    def setUp(self):
        self.user = User.objects.get(first_name="John")
        self.lesson_request = LessonRequest.objects.get(user=self.user)

    def test_valid_lesson_request(self):
        self._assert_lesson_request_is_valid()

    def test_is_available_on_monday_is_true_by_default(self):
        self.assertTrue(self.lesson_request.is_available_on_monday)

    def test_is_available_on_tuesday_is_true_by_default(self):
        self.assertTrue(self.lesson_request.is_available_on_tuesday)

    def test_is_available_on_wednesday_is_true_by_default(self):
        self.assertTrue(self.lesson_request.is_available_on_wednesday)

    def test_is_available_on_thursday_is_true_by_default(self):
        self.assertTrue(self.lesson_request.is_available_on_thursday)

    def test_is_available_on_friday_is_true_by_default(self):
        self.assertTrue(self.lesson_request.is_available_on_friday)

    def test_is_fulfilled_is_false_by_default(self):
        self.assertFalse(self.lesson_request.is_fulfilled)

    def test_no_of_lessons_cannot_be_blank(self):
        self.lesson_request.no_of_lessons = None

        self._assert_lesson_request_is_invalid()

    def test_lesson_interval_in_days_cannot_be_blank(self):
        self.lesson_request.lesson_interval_in_days = None

        self._assert_lesson_request_is_invalid()

    def test_lesson_duration_in_mins_cannot_be_blank(self):
        self.lesson_request.lesson_duration_in_mins = None

        self._assert_lesson_request_is_invalid()

    def test_further_information_can_be_blank(self):
        self.lesson_request.further_information = None

        self._assert_lesson_request_is_valid()

    def _assert_lesson_request_is_valid(self):
        try:
            self.lesson_request.full_clean()
        except ValidationError:
            self.fail("Test lesson request should be valid.")

    def _assert_lesson_request_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.lesson_request.full_clean()
