from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def required_active(view_func):
    """ Decorator which check if user is activated """
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('todolist:login')  # if user is not authenticated redirect him to login view
        if not request.user.is_active:
            # if user is not active redirect him to required_active template
            return redirect('todolist:required_active_user') 
        user_id = kwargs.get('user_id')
        if request.user.id != int(user_id):
            return HttpResponse('This is not your property')
        return view_func(request, *args, **kwargs)
    
    return login_required(_wrapped_view)