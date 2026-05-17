from django.shortcuts import render, redirect
from .forms import UserProfileForm
from .models import UserProfile
import json
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def userprofile(request):
    profile_types = []
    file_path = os.path.join(settings.BASE_DIR, 'usertype.json')
    with open(file_path) as json_file:
        data = json.load(json_file)
        for key, value in data.items():
            profile_types.append({'name': key, 'value': value})

    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        
        user_profile.profile_type = request.POST.get('profile_type')
        user_profile.email = request.POST.get('email')
        user_profile.phone = request.POST.get('phone')
        user_profile.city = request.POST.get('city')
        user_profile.date_of_birth = request.POST.get('date_of_birth')
        
        if 'profile_image' in request.FILES:
            user_profile.profile_image = request.FILES['profile_image']

        user_profile.save()

        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('userprofile')

    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        'profile_types': profile_types,
        'user_profile': user_profile,
        'form': form,
    }
    return render(request, 'userprofile/userProfile.html', context)




