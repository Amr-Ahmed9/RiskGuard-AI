from django.urls import path
from . import views

urlpatterns = [
    path('insights/', views.expenses_index, name='expenses_index'),
    path('tables/', views.expenses_tables, name='expenses-tables'),
    path('add-expenses/', views.add_expenses, name='add-expenses'),
    path('edit-expense/<int:expense_id>/', views.edit_expense, name='edit-expense'),
    path('delete-expense/<int:expense_id>/', views.delete_expense, name='delete-expense'),
    path('csv-download/', views.csv_download, name='csv-download'),
   
    path('pdf-download/', views.pdf_download, name='pdf-download'),
]
