from django import forms
from .models import Expense, Category


class ExpenseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()   
        self.fields['category'].label_from_instance = lambda obj: obj.name
    
    
    class Meta:
        model = Expense 

        fields = ['amount', 'date', 'description', 'category']  
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Amount',
                'step': '0.01'
            }),
            'date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter Description'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select Category'
            })
        }
