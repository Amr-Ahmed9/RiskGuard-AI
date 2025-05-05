from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    #URLS FOR THE REGISTRATION AND LOGIN AND LOGOUT
    path('register/',views.registerPage,name ='register'),
    path('login/',views.loginPage,name = 'login'),
    path('logout/',views.logoutUser,name ='logout'),
    
    #URLS FOR THE PASSWORD RESET
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='authentication/password_reset.html'), name='reset_password'),    
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'), name='password_reset_complete'),

    path('reset_password/', views.CustomPasswordResetForm, name='reset_password_Link'),
  
]