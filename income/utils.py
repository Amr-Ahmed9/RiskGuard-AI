from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import Income
from userpreferences.models import UserPreference

def income_data_processed(request):
 # Get or create user profile (same idea as UserPreference)
    user_preferences = UserPreference.objects.get_or_create(user=request.user)[0]
    incomes = Income.objects.filter(owner=request.user)
    
    # Get time period from request
    period = request.GET.get('period', 'monthly')
    
    # Total income (all time)
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0

    # Filter income by selected period
    now = timezone.now()
    if period == 'daily':
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        period_income = incomes.filter(date__gte=start_date).aggregate(Sum('amount'))['amount__sum'] or 0
    elif period == 'weekly':
        start_date = now - timedelta(days=now.weekday())
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        period_income = incomes.filter(date__gte=start_date).aggregate(Sum('amount'))['amount__sum'] or 0
    else:  # monthly
        start_date = now.replace(month=now.month, day=1, hour=0, minute=0, second=0, microsecond=0)
        period_income = incomes.filter().aggregate(Sum('amount'))['amount__sum'] or 0
    
    
    # Get distinct category count
    source_count = incomes.values('source').distinct().count()
    
    # Get recent income count
    recent_income_count = incomes.filter(date__gte=start_date).count()
    
    # Data for line chart
 
    
    dates = [income.date.strftime('%Y-%m-%d') for income in incomes.order_by('date')]
    amounts = [float(income.amount) for income in incomes.order_by('date')]
    

    # Data for pie chart by category
    sources = []
    source_amounts = []
    for source in incomes.values('source').annotate(total=Sum('amount')):
    
        sources.append(source['source'])
        source_amounts.append(float(source['total']))

    return {
        'total_income': total_income,
        'period_income': period_income,
        'source_count': source_count,
        'recent_income_count': recent_income_count,
        'dates': dates,
        'amounts': amounts,
        'sources': sources,
        'source_amounts': source_amounts,
        'user_preferences': user_preferences,
        'current_period': period,
        'now': now,
    }