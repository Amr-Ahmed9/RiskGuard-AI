
from django import forms
from .models import Income, Source

class IncomeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['source'].queryset = Source.objects.all()
        self.fields['source'].label_from_instance = lambda obj: obj.name

    class Meta:
        model = Income
        fields = ['amount', 'date', 'description', 'source']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter description'}),
            'source': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select source'}),
        }




