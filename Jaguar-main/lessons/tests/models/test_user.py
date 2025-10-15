from django.core.exceptions import ValidationError
from django.test import TestCase

from lessons.models import User


class TestUser(TestCase):
    fixtures_path = "lessons/tests/fixtures"
    fixtures = [f"{fixtures_path}/user_john.json", f"{fixtures_path}/user_jane.json"]

    def setUp(self):
        self.user_john = User.objects.get(first_name="John")
        self.user_jane = User.objects.get(first_name="Jane")

    def test_valid_user(self):
        self._assert_user_is_valid()

    def test_email_cannot_be_blank(self):
        self.user_john.email = ""

        self._assert_user_is_invalid()

    def test_email_must_be_unique(self):
        self.user_john.email = "jane.doe@example.org"

        self._assert_user_is_invalid()

    def test_role_is_student_by_default(self):
        self.assertEqual(self.user_john.role, "Student")

    def _assert_user_is_valid(self):
        try:
            self.user_john.full_clean()
        except ValidationError:
            self.fail("Test user should be valid.")

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user_john.full_clean()
