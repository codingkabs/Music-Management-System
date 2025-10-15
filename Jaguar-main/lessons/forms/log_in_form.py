from django import forms


class LogInForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={"placeholder": "e.g. yuri.gagarin@roscosmos.ru"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "e.g. tornado-human-radio-charge-even"}))
