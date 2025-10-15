from django.shortcuts import render
from django.urls import reverse

from lessons.helpers import get_invoice_amount
from lessons.models import Invoice


def invoices(request):
    # Generate correct list of invoices to show
    invoices = Invoice.objects.filter(user=request.user)

    def convert_invoice_to_card(invoice):
        heading = str(invoice)
        amount_due = get_invoice_amount(invoice)

        return {
            "heading":
                heading,
            "info": [{
                "title": "Amount Due",
                "description": amount_due,
            }, {
                "title": "Bank Reference",
                "description": heading
            }],
        }

    cards = map(convert_invoice_to_card, invoices)

    # Return page
    return render(
        request, "student/invoices.html", {
            "allowed_roles": ["Student"],
            "dashboard": {
                "heading": "Invoices",
                "subheading": "View the invoices for fulfilled lesson requests."
            },
            "cards": cards
        })
