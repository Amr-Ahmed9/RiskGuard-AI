from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import Expense
from userpreferences.models import UserPreference
def expense_data_processed(request):
    user_preferences = UserPreference.objects.get_or_create(user=request.user)[0]
    expenses = Expense.objects.filter(owner=request.user)
    
    # Get time period from request
    period = request.GET.get('period', 'monthly')
    
    # Calculate total expenses (all time)
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Calculate period expenses based on selection
    now = timezone.now()
    if period == 'daily':
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        period_expenses = expenses.filter(date__gte=start_date).aggregate(Sum('amount'))['amount__sum'] or 0
    elif period == 'weekly':
        start_date = now - timedelta(days=now.weekday())
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        period_expenses = expenses.filter(date__gte=start_date).aggregate(Sum('amount'))['amount__sum'] or 0
    else:  # monthly
        start_date = now.replace(month=now.month, day=1, hour=0, minute=0, second=0, microsecond=0)
        period_expenses = expenses.filter().aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Get category count
    category_count = expenses.values('category').distinct().count()
    
    # Get recent expenses count
    recent_expenses_count = expenses.filter(date__gte=start_date).count()
    
    # Prepare data for charts
    dates = [expense.date.strftime('%Y-%m-%d') for expense in expenses.order_by('date')]
    amounts = [float(expense.amount) for expense in expenses.order_by('date')]
    
    # Prepare data for pie chart
    categories = []
    category_amounts = []
    for category in expenses.values('category').annotate(total=Sum('amount')):
        categories.append(category['category'])
        category_amounts.append(float(category['total']))
    
    return {
        'total_expenses': total_expenses,
        'period_expenses': period_expenses,
        'category_count': category_count,
        'recent_expenses_count': recent_expenses_count,
        'dates': dates,
        'amounts': amounts,
        'categories': categories,
        'category_amounts': category_amounts,
        'user_preferences': user_preferences,
        'current_period': period,
        'now': now
    }