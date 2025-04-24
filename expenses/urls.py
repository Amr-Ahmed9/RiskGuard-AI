from django.urls import path
from . import views

urlpatterns = [
    path('insights/',views.expenses_index,name ='expenses_index'),
]
