from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm,User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate , login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
# Create your views here.
from .forms import CreatUserForm , LoginForm , ForgotPasswordForm
from .decorators import unauthenticated_user ,allowed_users
from .models import UserProfile


@unauthenticated_user
def registerPage(request):
    form = CreatUserForm()
    if request.method =='POST':
        form = CreatUserForm(request.POST)
        if form.is_valid():
            #  form.save()
            # user = form.cleaned_data.get('username')
            # messages.success(request , 'Account was created for ' + user)
            user = form.save()
            user_type = form.cleaned_data.get('user_type')
            UserProfile.objects.create(user=user, user_type=user_type)
            messages.success(request , 'Account was created for ' + user.username)
            return redirect('login')
    context = {'Rform':form}
    return render(request,'authentication/register.html',context)


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
                return redirect( 'expenses_index' )
            else:
                form.add_error(None, 'Invalid username or password')
                messages.info(request,'Invalid username or password')
    context ={'Lform':form}
    return render(request , 'authentication/login.html',context)



def forgotPassPage(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                # Ideally you use Django's password reset system, but here's a placeholder email logic
                send_mail(
                    subject='Reset Your Password',
                    message='Click the link below to reset your password:\nhttp://yourdomain.com/reset-link/',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                )
                messages.success(request, 'Password reset email sent!')
            else:
                messages.error(request, 'No user with this email was found.')
    else:
        form = ForgotPasswordForm()
    return render(request, 'forms/forgot-password.html', {'Fform': form})


# Logout View


def logoutUser(request):
    logout(request)
    return redirect('login')




# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages
# from .form import CreatUserForm, LoginForm

# # Registration View
# def registerPage(request):
#     form = CreatUserForm()

#     if request.method == 'POST':
#         form = CreatUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             email = form.cleaned_data.get('email')
#             messages.success(request, f'Account created for {email}')
#             return redirect('login')  # Change 'login' to your actual login route name if needed

#     context = {'Rform': form}
#     return render(request, 'forms/register.html', context)

# # Login View
# def loginPage(request):
#     form = LoginForm()

#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']

#             user = authenticate(request, email=email, password=password)

#             if user is not None:
#                 login(request, user)
#                 return redirect('homeforU')  # Change to your actual homepage name
#             else:
#                 form.add_error(None, 'Invalid email or password')

#     context = {'Lform': form}
#     return render(request, 'forms/login.html', context)

# # Logout View
# def logoutUser(request):
#     logout(request)
#     return redirect('login')
