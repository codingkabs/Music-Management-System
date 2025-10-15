from django import forms

from lessons.models import Term, User


class LessonRequestsFilterForm(forms.Form):
    # Status choices
    status_choices = [("all", "All"), ("unfulfilled", "Unfulfilled"), ("fulfilled", "Fulfilled")]

    # Fields
    student_filter = forms.ModelChoiceField(label="Filter by student:",
                                            queryset=User.objects.filter(role="Student", is_superuser=False),
                                            empty_label="All",
                                            required=False)

    term_filter = forms.ModelChoiceField(label="Filter by term:",
                                         queryset=Term.objects.all().order_by("-start_date"),
                                         empty_label="Any",
                                         required=False)

    status_filter = forms.CharField(label="Filter by status:", widget=forms.Select(choices=status_choices))
