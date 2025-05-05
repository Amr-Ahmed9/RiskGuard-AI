from django.urls import path    
from . import views

urlpatterns = [
    path('insights/', views.mainDash, name='mainDash'),

    path('create_target/', views.create_target, name='create_target'),
    path('edit_target/<int:target_id>/', views.edit_target, name='edit_target'),
    path('delete_target/<int:target_id>/', views.delete_target, name='delete_target'),
    
    path('set_alert/', views.set_alert, name='set_alert'),
    path('edit_alert/<int:alert_id>/', views.edit_alert, name='edit_alert'),
    path('delete_alert/<int:alert_id>/', views.delete_alert, name='delete_alert'),

    path('target_table/', views.tables, name='tables'),
    path('alert_table/', views.alerttable, name='alerttable'),
    path('overalltable/', views.overalltable, name='overalltable'),
    path('forecast/', views.forecast, name='forecast'),
 


]




