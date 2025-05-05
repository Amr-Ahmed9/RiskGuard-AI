
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

from income.models import Income
from expenses.models import Expense

def get_forecast_data(user, months_ahead=3):
    # Step 1: Load data
    income_qs = Income.objects.filter(owner=user)
    expense_qs = Expense.objects.filter(owner=user)

    income_df = pd.DataFrame(list(income_qs.values('amount', 'date')))
    expense_df = pd.DataFrame(list(expense_qs.values('amount', 'date')))

    if income_df.empty or expense_df.empty:
        return {'error': 'Not enough data to forecast.'}

    # Step 2: Convert dates to months
    income_df['date'] = pd.to_datetime(income_df['date']).dt.tz_localize(None)
    expense_df['date'] = pd.to_datetime(expense_df['date']).dt.tz_localize(None)

    income_df['month'] = income_df['date'].dt.to_period('M')
    expense_df['month'] = expense_df['date'].dt.to_period('M')

    income_monthly = income_df.groupby('month')['amount'].sum().reset_index()
    expense_monthly = expense_df.groupby('month')['amount'].sum().reset_index()

    # Step 3: Convert month to numerical for ML
    income_monthly['month_num'] = np.arange(len(income_monthly))
    expense_monthly['month_num'] = np.arange(len(expense_monthly))

    # Step 4: Train simple linear regression
    income_model = LinearRegression().fit(income_monthly[['month_num']], income_monthly['amount'])
    expense_model = LinearRegression().fit(expense_monthly[['month_num']], expense_monthly['amount'])

    # Step 5: Predict future months
    future_months = np.arange(len(income_monthly), len(income_monthly) + months_ahead)
    income_preds = income_model.predict(future_months.reshape(-1, 1))
    expense_preds = expense_model.predict(future_months.reshape(-1, 1))

    future_dates = [(income_monthly['month'].iloc[-1].to_timestamp() + pd.DateOffset(months=i+1)).strftime('%Y-%m') for i in range(months_ahead)]

    forecast = []
    for i in range(months_ahead):
        forecast.append({
            'month': future_dates[i],
            'predicted_income': round(income_preds[i], 2),
            'predicted_expense': round(expense_preds[i], 2),
            'net_savings': round(income_preds[i] - expense_preds[i], 2)
        })

    return forecast

