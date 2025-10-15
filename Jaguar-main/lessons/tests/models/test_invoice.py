from django.core.exceptions import ValidationError
from django.test import TestCase

from lessons.models import Invoice


class TestInvoice(TestCase):
    fixtures_path = "lessons/tests/fixtures"
    fixtures = [f"{fixtures_path}/invoice.json", f"{fixtures_path}/teacher.json"]

    def setUp(self):
        self.invoice = Invoice.objects.get(pk=1)

    def test_valid_invoice(self):
        self._assert_invoice_is_valid()

    def test_lesson_request_cannot_be_none(self):
        self.invoice.lesson_request = None
        self._assert_invoice_is_invalid()

    def test_user_cannot_be_none(self):
        self.invoice.user = None
        self._assert_invoice_is_invalid()

    def _assert_invoice_is_valid(self):
        try:
            self.invoice.full_clean()
        except ValidationError:
            self.fail("Test invoice should be valid.")

    def _assert_invoice_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.invoice.full_clean()