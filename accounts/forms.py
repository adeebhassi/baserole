# accounts/forms.py
from django import forms
from .models import User, Role

class RoleSelectionForm(forms.Form):
    role = forms.ModelChoiceField(queryset=Role.objects.none(), empty_label="Select Role")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['role'].queryset = user.roles.all()
