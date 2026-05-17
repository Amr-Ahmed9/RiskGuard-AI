from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

#note DR.
# i created this model to create a target for the user to achieve but i fixed it in the views.py file to make it easier to use tutor and thanks
class Target(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    TARGET_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('savings', 'Savings'),
        ('net_profit', 'Net Profit'),
    ]
    target_type = models.CharField(max_length=20, choices=TARGET_TYPES)
    amount = models.FloatField(validators=[MinValueValidator(0)])
    PERIOD_CHOICES = [
        ('daily', 'Day'),
        ('weekly', 'Week'),
        ('monthly', 'Month'),
        ('yearly', 'Year'),
    ]
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.target_type} target"

class AlertSetting(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=50, default='expense_increase')
    frequency = models.CharField(max_length=10, choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s alert settings"
  