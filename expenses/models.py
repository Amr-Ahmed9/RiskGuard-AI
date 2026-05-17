from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.validators import MinValueValidator
# Create your models here.
class Expense(models.Model):
    amount = models.FloatField(
        validators=[MinValueValidator(0)]
    )
    date = models.DateTimeField(default=now)    
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    

    CHOICES_CATEGORIES = [
                ('Housing', 'Housing'),
                ('Transportation', 'Transportation'),
                ('Food', 'Food'),
                ('Health & Fitness', 'Health & Fitness'),
                ('Debt Payments', 'Debt Payments'),
                ('Entertainment', 'Entertainment'),
                ('Education', 'Education'),
                ('Personal Care', 'Personal Care'),
                ('Savings & Investments', 'Savings & Investments'),
                ('Gifts & Donations', 'Gifts & Donations'),
                ('Travel', 'Travel'),
                ('Subscriptions', 'Subscriptions'),
                ('Miscellaneous', 'Miscellaneous'),
                ('Loan Payments', 'Loan Payments'),
                ('Bad Debt', 'Bad Debt'),
                ('Fees', 'Fees'),
                ('Taxes',  'Taxes'),
                ('Insurance', 'Insurance'),
                ('Other', 'Other'),
               
            ]
    category = models.CharField(max_length=50, choices=CHOICES_CATEGORIES)
        
    def __str__(self):
        return self.category

    class Meta:
        ordering = ['-date']    


class Category(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name