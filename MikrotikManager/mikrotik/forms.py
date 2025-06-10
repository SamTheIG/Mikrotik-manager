from django import forms
from .models import Mikrotik

class addMikuserForm(forms.Form):
    device = forms.ModelChoiceField(queryset=Mikrotik.objects.none())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['device'].queryset = Mikrotik.objects.filter(Userid=user.id)
