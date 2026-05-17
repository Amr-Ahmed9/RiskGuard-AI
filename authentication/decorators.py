
from django.shortcuts import redirect

#THE CONTROL ABOUT USER AUTHENTICATION 
def unauthenticated_user(view_func):
    def wrappar_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('mainDash')
        else:
            return view_func(request,*args,**kwargs)
    return wrappar_func    


