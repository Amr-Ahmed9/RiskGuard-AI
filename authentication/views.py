from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
# Create your views here.
from .forms import CreatUserForm , LoginForm 
from .decorators import unauthenticated_user 
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

#register view
@unauthenticated_user
def registerPage(request):
    form = CreatUserForm()

    if request.method =='POST':
        form = CreatUserForm(request.POST)
        if form.is_valid():
            user = form.save() 

            messages.success(request , 'Account was created for ' + user.username)
            return redirect('login')
    context = {'Rform':form}
    return render(request,'authentication/register.html',context)


#login view 
@unauthenticated_user
def loginPage(request):

    form = LoginForm()
    if request.method == 'POST':
        form =LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request , username=username ,password=password)
            if user is not None :
                login(request ,user)
                messages.success(request, "Welcome to the main dashboard!")
                return redirect( 'mainDash' )
            else:
                messages.info(request,'Invalid username or password')
                return redirect('login')
    context ={'Lform':form}
    return render(request , 'authentication/login.html',context)






def CustomPasswordResetForm(request):
        def save(self, request, **kwargs):
            email = self.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)

                reset_url = f"http://127.0.0.1:8000/authentication/reset/{uid}/{token}/"
                return render(request, 'authentication/password_reset_display.html', {'reset_url': reset_url})

            except User.DoesNotExist:
                return render(request, 'authentication/password_reset_display.html', {'error': "User not found."})


# Logout View

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

