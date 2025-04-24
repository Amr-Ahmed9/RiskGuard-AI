from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrappar_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('expenses_index')
        else:
            return view_func(request,*args,**kwargs)
    return wrappar_func    


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrappar_func(request,*args,**kwargs):
            
            print('working',allowed_users)
            return view_func(request,*args,**kwargs)
        return wrappar_func
    return decorator