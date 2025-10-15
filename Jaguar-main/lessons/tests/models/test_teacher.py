from django.core.exceptions import ValidationError
from django.test import TestCase

from lessons.models import Teacher


class TestTeacher(TestCase):
    fixtures = ["lessons/tests/fixtures/teacher.json"]

    def setUp(self):
        self.teacher = Teacher.objects.get(first_name="Daniel")

    def test_valid_teacher(self):
        self._assert_teacher_is_valid()

    def test_first_name_cannot_be_none(self):
        self.teacher.first_name = None
        self._assert_teacher_is_invalid()

    def test_last_name_cannot_be_none(self):
        self.teacher.last_name = None
        self._assert_teacher_is_invalid()

    def _assert_teacher_is_valid(self):
        try:
            self.teacher.full_clean()
        except ValidationError:
            self.fail("Test teacher should be valid.")

    def _assert_teacher_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.teacher.full_clean()