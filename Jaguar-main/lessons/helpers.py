import locale

from lessons.models import Invoice, Lesson, User, Payment

LESSON_PRICE_MULTIPLIER = 1.15


def get_lesson_price(lesson):
    locale.setlocale(locale.LC_ALL, 'en_GB')
    return locale.currency(lesson.duration * LESSON_PRICE_MULTIPLIER, grouping=True)


def get_invoice_amount(invoice):
    # Find the lessons that match the lesson request of this invoice
    lessons = Lesson.objects.filter(lesson_request=invoice.lesson_request)

    total_amount = 0

    for lesson in lessons:
        total_amount = total_amount + float(get_lesson_price(lesson)[1:])

    locale.setlocale(locale.LC_ALL, 'en_GB')
    return locale.currency(total_amount, grouping=True)


def get_balance_for_student(student):
    assert isinstance(student, User)
    assert student.role == "Student"

    amount_owed = 0
    amount_paid = 0
    difference = 0

    # Calculate amount owed
    invoices_belonging_to_student = Invoice.objects.filter(user=student)

    for invoice in invoices_belonging_to_student:
        invoice_amount = float(get_invoice_amount(invoice)[1:])  # Strip £ sign

        amount_owed = amount_owed + invoice_amount

    # Calculate amount paid
    payments_from_student = Payment.objects.filter(user=student)

    for payment in payments_from_student:
        amount_paid = amount_paid + float(payment.amount_paid)

    # Return difference
    difference = amount_owed - amount_paid

    locale.setlocale(locale.LC_ALL, 'en_GB')
    return locale.currency(difference, grouping=True)