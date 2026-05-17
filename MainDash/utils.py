from django.core.cache import cache
from income.models import Income
from expenses.models import Expense
from userpreferences.models import UserPreference
from .models import Target
from django.db.models import Sum, F, Avg
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import json
import calendar

def dashboard_data(request):
    user = request.user
    now = timezone.now()

   
    user_preferences = UserPreference.objects.get_or_create(user=request.user)[0]
    time_filter = request.GET.get('time_filter', 'month')
    

    
    # Date range handling
    date_ranges = {
        'day': now - timedelta(days=1),
        'week': now - timedelta(days=7),
        'month': now - timedelta(days=30),
        'year': now - timedelta(days=365),
        'all': None,
    }
    start_date = date_ranges.get(time_filter, now - timedelta(days=30))

    # Querysets
    income_qs = Income.objects.filter(owner=user, date__gte=start_date) if start_date else Income.objects.filter(owner=user)
    expense_qs = Expense.objects.filter(owner=user, date__gte=start_date) if start_date else Expense.objects.filter(owner=user)
    
   
    # Financial calculations
    try:
     # Just in case net profit exceeds goal

    # Calculate the average income and expenses
   
        avrage_income = income_qs.aggregate(Avg('amount'))['amount__avg'] or 0
        avrage_expenses = expense_qs.aggregate(Avg('amount'))['amount__avg'] or 0
        total_income = income_qs.aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = expense_qs.aggregate(Sum('amount'))['amount__sum'] or 0
        net_profit = total_income - total_expenses
        expense_ratio = (total_expenses / total_income * 100) if total_income else 0
        income_ratio = (total_income / total_expenses * 100) if total_expenses else 0
        
    except Exception as e:
        total_income = total_expenses = net_profit =  0
        messages.error(request, f"Error calculating financial metrics: {str(e)}")

    # Alerts (Expense increase compared to previous period)
    alerts = []
    try:
        last_period_start = None
        last_period_end = None

        if time_filter == 'day':
            last_period_start = now - timedelta(days=2)
            last_period_end = now - timedelta(days=1)
        elif time_filter == 'week':
            last_period_start = now - timedelta(days=14)
            last_period_end = now - timedelta(days=7)
        elif time_filter == 'month':
            last_period_start = now - timedelta(days=60)
            last_period_end = now - timedelta(days=30)
       
        if last_period_start and last_period_end:
            last_period_expense = Expense.objects.filter(
                owner=user, date__gte=last_period_start, date__lt=last_period_end
            ).aggregate(Sum('amount'))['amount__sum'] or 0

            current_expense = expense_qs.aggregate(Sum('amount'))['amount__sum'] or 0

            if last_period_expense > 0:
                increase_percent = ((current_expense - last_period_expense) / last_period_expense) * 100
                if increase_percent > 20:
                    alerts.append(f"Warning: Your expenses increased by {increase_percent:.1f}% compared to the previous period!")
    
    except Exception as e:
        messages.error(request, f"Error calculating alerts: {str(e)}")

    # Chart data for pie and line and avarage
   
    income_data = []    
    expense_data = []
    cash_flow_data = []
    months = []
    expense_categories = []
    growth_rate_data = []
    try:
        if time_filter == 'day':
            # Group by hour
            income_data = list(income_qs.values('date__hour').annotate(
                label=F('date__hour'),
                total=Sum('amount')
            ).order_by('label'))

            expense_data = list(expense_qs.values('date__hour').annotate(
                label=F('date__hour'),
                total=Sum('amount')
            ).order_by('label'))

            average_income = sum(income.get('total', 0) for income in income_data) / len(income_data) if income_data else 0
            average_expense = sum(expense.get('total', 0) for expense in expense_data) / len(expense_data) if expense_data else 0

            
          
            for i in range(1, len(income_data)):
                previous_ratio = (income_data[i-1].get('total', 0) or 0) / (expense_data[i-1].get('total', 0) or 0) * 100
                current_ratio = (income_data[i].get('total', 0) or 0) / (expense_data[i].get('total', 0) or 0) * 100
                
                # Calculate the growth rate based on the previous ratio
                if previous_ratio != 0:
                    growth_rate = (current_ratio - previous_ratio) / previous_ratio * 100
                else:
                    growth_rate = 0  # No growth if the previous ratio is 0
                
                growth_rate_data.append(growth_rate)
            # daviation_data = [float(income.get('total', 0) or 0) - float(expense.get('total', 0) or 0) for income, expense in zip(income_data, expense_data)]
            
            months = [f"{entry['label']}:00" for entry in income_data]  # "13:00", "14:00"
        elif time_filter == 'week' or time_filter == 'month':
            # Group by day
            income_data = list(income_qs.values('date__day').annotate(
                label=F('date__day'),
                total=Sum('amount')
            ).order_by('label'))

            expense_data = list(expense_qs.values('date__day').annotate(
                label=F('date__day'),
                total=Sum('amount')
            ).order_by('label'))
           

            average_income = sum(income.get('total', 0) for income in income_data) / len(income_data) if income_data else 0
            average_expense = sum(expense.get('total', 0) for expense in expense_data) / len(expense_data) if expense_data else 0

            for i in range(1, len(income_data)):
                previous_ratio = (income_data[i-1].get('total', 0) or 0) / (expense_data[i-1].get('total', 0) or 0) * 100
                current_ratio = (income_data[i].get('total', 0) or 0) / (expense_data[i].get('total', 0) or 0) * 100
                
                # Calculate the growth rate based on the previous ratio
                if previous_ratio != 0:
                    growth_rate = (current_ratio - previous_ratio) / previous_ratio * 100
                else:
                    growth_rate = 0  # No growth if the previous ratio is 0
                
                growth_rate_data.append(growth_rate)

            months = [f"Day {entry['label']}" for entry in income_data]
        else:
            # Default group by month
            income_data = list(income_qs.values('date__month').annotate(
                label=F('date__month'),
                total=Sum('amount')
            ).order_by('label'))

            expense_data = list(expense_qs.values('date__month').annotate(
                label=F('date__month'),
                total=Sum('amount')
            ).order_by('label'))

            average_income = sum(income.get('total', 0) for income in income_data) / len(income_data) if income_data else 0
            average_expense = sum(expense.get('total', 0) for expense in expense_data) / len(expense_data) if expense_data else 0
            

            for i in range(1, len(income_data)):
                previous_ratio = (income_data[i-1].get('total', 0) or 0) / (expense_data[i-1].get('total', 0) or 0) * 100
                current_ratio = (income_data[i].get('total', 0) or 0) / (expense_data[i].get('total', 0) or 0) * 100
                
                # Calculate the growth rate based on the previous ratio
                if previous_ratio != 0:
                    growth_rate = (current_ratio - previous_ratio) / previous_ratio * 100
                else:
                    growth_rate = 0  # No growth if the previous ratio is 0
                
                growth_rate_data.append(growth_rate)

            months = [calendar.month_name[entry['label']] for entry in income_data]

        

        cash_flow_data = [
            (income.get('total', 0) or 0) / (expense.get('total', 0) or 0) * 100
            for income, expense in zip(income_data, expense_data)
        ]
    except Exception as e:
        messages.error(request, f"Error generating chart data: {str(e)}")

 

    goals = []   
    can_spend = []
    
    try:
        savings_goal = Target.objects.filter(user=user).first()
        if savings_goal and savings_goal.amount > 0:
            goal_percent = (net_profit / savings_goal.amount) * 100
            goals.append(f"You're {goal_percent:.1f}% toward your savings goal!")

            canspend = net_profit - savings_goal.amount
            if canspend >= 0:
                can_spend.append(
                    f"Your savings goal is {savings_goal.amount:.1f} and your net profit is {net_profit:.1f}. "
                    f"You can safely spend {canspend:.1f} and still meet your goal."
                )
            else:
                can_spend.append(
                    f"Your savings goal is {savings_goal.amount:.1f} but your net profit is only {net_profit:.1f}. "
                    f"You are short by {-canspend:.1f} to meet your goal."
                )
    except Exception as e:
        messages.error(request, f"Error calculating goal tracking: {str(e)}")

    
    dates = [income.date.strftime('%Y-%m-%d') for income in income_qs.order_by('date')]
    amounts = [float(income.amount) for income in income_qs.order_by('date')]
    amounts_expenses = [float(expense.amount) for expense in expense_qs.order_by('date')]

    

    return {
        'user_preferences': user_preferences,
        'avrage_income': avrage_income,
        'avrage_expenses': avrage_expenses,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'average_income': average_income,
        'average_expense': average_expense,
        'net_profit': net_profit,
        'cash_flow': "Positive" if net_profit >= 0 else "Negative",
        'can_spend': can_spend,
        'income_ratio': income_ratio,
        'expense_ratio': expense_ratio,
        'alerts': alerts,
        'goals': goals, 
        'dates': dates,
        'amounts': amounts, 
        'amounts_expenses': amounts_expenses,
        
        'growth_rate_data': json.dumps(growth_rate_data),
        'savings_goal_amount':savings_goal.amount if savings_goal else 0,
        'income_data': json.dumps(income_data),
        'expense_data': json.dumps(expense_data),
        'expense_categories': json.dumps(expense_categories),
        'cash_flow_data': json.dumps(cash_flow_data),
        'months': json.dumps(months),
        'time_filter': time_filter,
        'user_preferences': user_preferences,
        
        
    }


