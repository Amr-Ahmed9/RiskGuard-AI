from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import IncomeForm
from .models import Income
from django.contrib.auth.decorators import login_required
from .utils import income_data_processed
from userpreferences.models import UserPreference
from django.http import HttpResponse
import csv
from datetime import datetime



@login_required(login_url='login')
def income_index(request):
    data = income_data_processed(request)
    return render(request, 'income/index.html',data)


@login_required(login_url='login')
def add_income(request):
   
    
    user_preferences = UserPreference.objects.get_or_create(user=request.user)[0]
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.owner = request.user
            income.save()
            messages.success(request, 'Income added successfully')
            return redirect('income_index')
    else:
        messages.error(request, 'Invalid form data')
        form = IncomeForm()

        context = {
            'form': form,
            'user_preferences': user_preferences,
        }
    return render(request, 'income/add-income.html', context)

@login_required(login_url='login')
def edit_income(request, income_id):
    user_preferences = UserPreference.objects.get_or_create(user=request.user)[0]
    income = get_object_or_404(Income, id=income_id, owner=request.user)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            messages.success(request, 'Income updated successfully')
            return redirect('income_tables')
    else:
        messages.error(request, 'Invalid form data')
        form = IncomeForm(instance=income)

        context = {
            'form': form,
            'user_preferences': user_preferences,
            'income': income,
        }
    return render(request, 'income/edit-income.html', context)


@login_required(login_url='login')
def delete_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, owner=request.user)
    income.delete() 
    messages.success(request, 'Income deleted successfully')
    return redirect('income_tables')


@login_required(login_url='login')  
def income_tables(request):
    user_preferences = UserPreference.objects.get_or_create(user=request.user)[0]
    incomes = Income.objects.filter(owner=request.user)
    context = {
        'incomes': incomes,
        'user_preferences': user_preferences,
    }
    return render(request, 'income/tables.html', context)


@login_required(login_url='login')
def csv_downloa(request):
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename=Income' +\
      datetime.now().strftime("%Y-%m-%d")+'.csv'
  writer = csv.writer(response)
  writer.writerow(['Amount','Date','Description', 'Source'])
  for income in Income.objects.filter(owner=request.user):
    writer.writerow([income.amount, income.date, income.description, income.source])
  return response
        
      

@login_required(login_url='login')
def pdf_downloa(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Income' +\
        datetime.now().strftime("%Y-%m-%d")+'.pdf'
    return response