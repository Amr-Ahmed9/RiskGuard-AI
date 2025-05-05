from django.urls import path
from . import views

urlpatterns = [
    path('insights/', views.income_index, name='income_index'),
    path('tables/', views.income_tables, name='income_tables'),
    path('add/', views.add_income, name='add_income'),
    path('edit/<int:income_id>/', views.edit_income, name='edit_income'),
    path('delete/<int:income_id>/', views.delete_income, name='delete_income'),
]
