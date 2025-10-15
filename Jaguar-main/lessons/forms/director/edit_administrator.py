from django import forms

from lessons.models import User


class AdminEditForm(forms.ModelForm):

    class Meta:

        model = User
        fields = ("email", "first_name", "last_name", "role")