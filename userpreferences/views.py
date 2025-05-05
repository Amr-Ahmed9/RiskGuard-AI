from django.shortcuts import render,redirect
import json
import os
from django.conf import settings
from .forms import UserPreferenceForm
from .models import UserPreference
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='login')  
def index(request):
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    with open(file_path) as json_file:
        data = json.load(json_file)
        for key, value in data.items():
            currency_data.append({'name': key, 'value': value})
    
    user_preferences = UserPreference.objects.get_or_create(user=request.user)[0]
    
    if request.method == 'POST':
        form = UserPreferenceForm(request.POST, instance=user_preferences)
        if form.is_valid():
            form.save()
            return redirect('userpreferences')
    else:
        form = UserPreferenceForm(instance=user_preferences)
         

        context = {
                'currencies': currency_data,
                'form': form,
                'user_preference': user_preferences
            }
    
    return render(request, 'userpreferences/index.html', context)

