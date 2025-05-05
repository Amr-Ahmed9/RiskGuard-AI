from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import dashboard_data
from userpreferences.models import UserPreference
from .forms import TargetForm, AlertSettingForm
from .models import Target, AlertSetting
from .forecasting import get_forecast_data
from django.http import HttpResponse
import csv
from datetime import datetime


@login_required(login_url='login')
def mainDash(request):
    
    context = dashboard_data(request)
    return render(request, 'MainDash/mainDash.html', context)

@login_required(login_url='login')
def create_target(request):
    user_preferences = UserPreference.objects.get_or_create(user=request.user)[0]
    if request.method == 'POST':
        form = TargetForm(request.POST)
        if form.is_valid():
            target = form.save(commit=False)    
            target.user = request.user
            target.save()
            messages.success(request, "Target set successfully!")
            return redirect('mainDash')
        else:
            messages.error(request, "Error setting target!")
            return redirect('create_target')

    else:
        form = TargetForm()
        context = {'form': form,
                   'user_preferences': user_preferences}
        return render(request, 'MainDash/create_target.html', context)
   

@login_required(login_url='login')
def edit_target(request, target_id):
    user_preferences = UserPreference.objects.get_or_create(user=request.user)[0]
   
    target = get_object_or_404(Target, id=target_id, user=request.user)
    if request.method == 'POST':
        form = TargetForm(request.POST, instance=target)
        if form.is_valid():
            form.save()
            messages.success(request, "Target updated successfully!")
            return redirect('tables')
   
    else:
        messages.error(request, 'Invalid form data')
        form = TargetForm(instance=target)
        context = {'form': form, 
                   'user_preferences': user_preferences,
                    'target': target,
                   
        }
    return render(request, 'MainDash/edit_target.html', context)


@login_required(login_url='login')
def delete_target(request, target_id):
    target = get_object_or_404(Target, id=target_id, user=request.user)
    target.delete()
    messages.success(request, "Target deleted successfully!")
    return redirect('tables')


@login_required(login_url='login')
def set_alert(request):
    if request.method == 'POST':
        form = AlertSettingForm(request.POST)
        if form.is_valid():
            alert = form.save(commit=False)
            alert.user = request.user
            alert.save()
            messages.success(request, "Alert settings updated successfully!")
            return redirect('mainDash')
        else:
            messages.error(request, "Error setting alert!")
            return redirect('set_alert')
    else:
        form = AlertSettingForm()
        context = {'form': form}
        return render(request, 'MainDash/set_alert.html', context)


@login_required(login_url='login')
def edit_alert(request, alert_id):
    alert = get_object_or_404(AlertSetting, id=alert_id, user=request.user)
    if request.method == 'POST':
        form = AlertSettingForm(request.POST, instance=alert)
        if form.is_valid():
            form.save()
            messages.success(request, "Alert updated successfully!")
            return redirect('alerttable')
       
    else:
        messages.error(request, 'Invalid form data')
        form = AlertSettingForm(instance=alert)
        context = {'form': form,
                   'alert': alert,
                   }
        return render(request, 'MainDash/edit_alert.html', context)


@login_required(login_url='login')
def delete_alert(request, alert_id):
    alert = get_object_or_404(AlertSetting, id=alert_id, user=request.user)
    alert.delete()
    messages.success(request, "Alert deleted successfully!")
    return redirect('alerttable')


@login_required(login_url='login')
def alerttable(request):
    alert = AlertSetting.objects.filter(user=request.user)
    context = {'alert': alert,
               }
    return render(request, 'MainDash/alerttable.html', context)

@login_required(login_url='login')

def tables(request):
    user_preferences = UserPreference.objects.get_or_create(user=request.user)[0]
    target = Target.objects.filter(user=request.user)
    context = {'target': target,
               'user_preferences': user_preferences}
    return render(request, 'MainDash/tables.html', context)



@login_required(login_url='login')
def overalltable(request):
    data = dashboard_data(request)
    return render(request, 'MainDash/overalltable.html', data)




@login_required(login_url='login')
def forecast(request):
    user_preferences = UserPreference.objects.get_or_create(user=request.user)[0]
    forecast_data = get_forecast_data(request.user)
    context = {'forecast_data': forecast_data,
               'user_preferences': user_preferences}
    return render(request, 'MainDash/forecast.html', context)


import csv
from datetime import datetime
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def csv_download(request):
    # Assuming 'dashboard_data' returns a dictionary with all the necessary data
    data = dashboard_data(request)
    
    # Set up the CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Income_' + datetime.now().strftime("%Y-%m-%d") + '.csv'
    
    # Create a CSV writer object
    writer = csv.writer(response)
    
    # Write the headers in the first row (optional)
    writer.writerow(['Field', 'Value'])
    
    # Write the data fields and their corresponding values
    writer.writerow(['Saving Goal', f"{data['goals']} {data['user_preferences'].currency}"])
    writer.writerow(['Total Income', f"{data['total_income']} {data['user_preferences'].currency}"])
    writer.writerow(['Total Expenses', f"{data['total_expenses']} {data['user_preferences'].currency}"])
    writer.writerow(['Net Profit', f"{data['net_profit']} {data['user_preferences'].currency}"])
    writer.writerow(['Average Income', f"{data['average_income']} {data['user_preferences'].currency}"])
    writer.writerow(['Average Expenses', f"{data['average_expense']} {data['user_preferences'].currency}"])
    writer.writerow(['Income Ratio', f"{data['income_ratio']}%"])
    writer.writerow(['Expenses Ratio', f"{data['expense_ratio']}%"])
    
    return response

      

@login_required(login_url='login')
def pdf_download(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Income' +\
        datetime.now().strftime("%Y-%m-%d")+'.pdf'
    return response
