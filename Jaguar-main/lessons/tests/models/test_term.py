from django.core.exceptions import ValidationError
from django.test import TestCase

from lessons.models import Term


class TestTerm(TestCase):
    fixtures = ["lessons/tests/fixtures/term.json"]

    def setUp(self):
        self.term = Term.objects.get(pk=1)

    def test_valid_term(self):
        self._assert_term_is_valid()

    def test_order_cannot_be_none(self):
        self.term.order = None
        self._assert_term_is_invalid()

    def test_start_date_cannot_be_none(self):
        self.term.start_date = None
        self._assert_term_is_invalid()

    def test_end_date_cannot_be_none(self):
        self.term.end_date = None
        self._assert_term_is_invalid()

    def _assert_term_is_valid(self):
        try:
            self.term.full_clean()
        except ValidationError:
            self.fail("Test term should be valid.")

    def _assert_term_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.term.full_clean()