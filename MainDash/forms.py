from django import forms
from .models import Target, AlertSetting
class TargetForm(forms.ModelForm):
    class Meta:

        model = Target
        fields = ['amount', 'period', 'start_date', 'end_date']
        widgets = {
            
            'period': forms.Select(choices=[
                ('daily', 'Day'),
                ('weekly', 'Week'),
                ('monthly', 'Month'),
                ('yearly', 'Year'),
            ],attrs={'class': 'form-control', 'placeholder': 'Select the period'}),
            
            'amount': forms.NumberInput(attrs={'min': 0, 'placeholder': 'Enter the target amount'}),

            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': False}),
        }
        # Add clean methods to TargetForm
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Amount must be positive")
        return amount

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if end_date and end_date < start_date:
            raise forms.ValidationError("End date cannot be before start date")

class AlertSettingForm(forms.ModelForm):
    class Meta:
        model = AlertSetting
        fields = ['frequency', 'alert_type','is_active']
        widgets = {
            'frequency': forms.Select(choices=[
                ('daily', 'Daily'),
                ('weekly', 'Weekly'),
                ('monthly', 'Monthly'),
            ],attrs={'class': 'form-control', 'placeholder': 'Select the frequency'}),
           
             'alert_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the alert type'}),
           
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input' ,
                                                    'style': 'width: 20px; height: 20px;'}),
        }
    def clean_frequency(self):
        frequency = self.cleaned_data.get('frequency')
        if frequency not in ['daily', 'weekly', 'monthly']:
            raise forms.ValidationError("Invalid frequency")
        return frequency
    


