from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
from django.core.validators import MinValueValidator

class Income(models.Model):
    
    amount = models.FloatField(validators=[MinValueValidator(0)])
    date = models.DateTimeField(default=timezone.now, editable=True)
    description = models.TextField()
    
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    
    PROFILE_INCOME_SOURCES = [
    ("Salary", "Salary"),
    ("Bonus", "Bonus"),
    ("Overtime", "Overtime"),
    ("Commission", "Commission"),
    ("Business Revenue", "Business Revenue"),
    ("Product Sales", "Product Sales"),
    ("Service Income", "Service Income"),
    ("Investment Returns", "Investment Returns"),
    ("Project Payment", "Project Payment"),
    ("Client Payment", "Client Payment"),
    ("Gig Income", "Gig Income"),
    ("Allowance", "Allowance"),
    ("Miscellaneous", "Miscellaneous"),
    ("Gifts", "Gifts"),
    ("Grants", "Grants"),
    ("Loan", "Loan"),
    ("Dividends", "Dividends"),
    ("Rental Income", "Rental Income"),
    ("Interest Income", "Interest Income"),
    ("Refunds", "Refunds"),
    ("Other", "Other"),

    ]
    
    source = models.CharField(max_length=50, choices=PROFILE_INCOME_SOURCES )
    
    
    def __str__(self):
        return self.source

    class Meta:
        ordering = ['-date']



class Source(models.Model):
    
    name = models.CharField(max_length=50)
    
    class Meta:
        verbose_name_plural = 'Sources'


    def __str__(self):
        return self.name

  
