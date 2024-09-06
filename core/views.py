from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from core.forms import RegisterForm
from django.contrib import messages

def index(request):
    return render(request,'partials/index.html')

def about(request):
    return render(request,'partials/about.html')

def contact(request):
    return render(request,'partials/contact.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('catalogue:index')  
    else:
        form = RegisterForm()
    
    return render(request, 'partials/register.html', {'form': form})