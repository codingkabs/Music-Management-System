from django import forms

from lessons.models import User


class TransactionFilterForm(forms.Form):
    """A form used to filter transactions by a single selected student and transaction type (balance, invoice or payment)."""
    transaction_choices = [("balances", "Balances"), ("invoices", "Invoices"), ("payments", "Payments")]

    student_filter = forms.ModelChoiceField(label="Filter by student:",
                                            queryset=User.objects.filter(role="Student", is_superuser=False),
                                            empty_label="All",
                                            required=False)

    transaction_filter = forms.CharField(label="Filter by type:", widget=forms.Select(choices=transaction_choices))