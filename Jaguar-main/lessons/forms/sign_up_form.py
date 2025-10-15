from django import forms

from lessons.models import User


class SignUpForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "e.g. Yuri"}),
            "last_name": forms.TextInput(attrs={"placeholder": "e.g. Gagarin"})
        }

    email = forms.EmailField(label="Email",
                             widget=forms.TextInput(attrs={"placeholder": "e.g. yuri.gagarin@roscosmos.ru"}))

    new_password = forms.CharField(
        label="New password", widget=forms.PasswordInput(attrs={"placeholder": "e.g. tornado-human-radio-charge-even"}))

    password_confirmation = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={"placeholder": "e.g. tornado-human-radio-charge-even"}))

    def clean(self):
        super().clean()

        new_password = self.cleaned_data.get("new_password")
        password_confirmation = self.cleaned_data.get("password_confirmation")

        if new_password != password_confirmation:
            self.add_error("password_confirmation", "Confirmation does not match password.")

    def save(self, commit=True):
        super().save(commit=False)

        user = User.objects.create_user(
            self.cleaned_data.get("email"),
            password=self.cleaned_data.get("new_password"),
            first_name=self.cleaned_data.get("first_name"),
            last_name=self.cleaned_data.get("last_name"),
            role="Student",  # Any user created via sign up form should be a student
        )

        return user
