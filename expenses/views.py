from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Expense
from .forms import ExpenseForm
from userpreferences.models import UserPreference
from django.contrib import messages
from .utils import expense_data_processed
from django.http import HttpResponse
from datetime import datetime
import csv

@login_required(login_url='login')

def expenses_index(request):
    data = expense_data_processed(request)
    return render(request, 'expenses/index.html', data)

@login_required(login_url='login')
def expenses_tables(request):
    user_preferences = UserPreference.objects.get_or_create(user=request.user)[0]
    expenses = Expense.objects.filter(owner=request.user)
    context = {
        'expenses': expenses,
        'user_preferences': user_preferences
    }
    return render(request, 'expenses/tables.html', context)

@login_required(login_url='login')
def add_expenses(request):
    user_preferences = UserPreference.objects.get_or_create(user=request.user)[0]
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.owner = request.user
            expense.save()
            messages.success(request, 'Expense added successfully')
            return redirect('expenses_index')
    else:
        messages.error(request, 'Invalid form data')
        form = ExpenseForm()
        
        context = {
            'form': form,
            'user_preferences': user_preferences
        }
    return render(request,'expenses/add-expenses.html',context)
    
    


@login_required(login_url='login')
def edit_expense(request, expense_id):
    user_preferences = UserPreference.objects.get_or_create(user=request.user)[0]
    expense = get_object_or_404(Expense, pk=expense_id, owner=request.user)
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully')
            return redirect('expenses-tables')
    else:
        messages.error(request, 'Invalid form data')
        form = ExpenseForm(instance=expense)
    
    context = {
        'form': form,
        'user_preferences': user_preferences,
        'expense': expense
    }
    return render(request, 'expenses/edit-expense.html', context)

@login_required(login_url='login')
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id, owner=request.user)
    expense.delete()
    messages.success(request, 'Expense deleted successfully')
    return redirect('expenses-tables')   

@login_required(login_url='login')
def csv_download(request):
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename=Expenses' +\
      datetime.now().strftime("%Y-%m-%d")+'.csv'
  writer = csv.writer(response)
  writer.writerow(['Amount','Date','Description', 'Category'])
  for expense in Expense.objects.filter(owner=request.user):
    writer.writerow([expense.amount, expense.date, expense.description, expense.category])
  return response
        
      

@login_required(login_url='login')
def pdf_download(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Expenses' +\
        datetime.now().strftime("%Y-%m-%d")+'.pdf'
    return response

