from django.urls import path
from . import views

urlpatterns = [
    path('ofuser/', views.index, name='userpreferences'),
    # path('update_preferences/', views.update_preferences, name='update_preferences'),   
    # path('save_user_preferences/', views.save_user_preferences, name='save_user_preferences'),
]
