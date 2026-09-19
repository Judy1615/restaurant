from django.shortcuts import render

def home(request):
    return render(request, 'pages/home.html')

def contact(request):
    return render(request, 'pages/contact.html')

from django.contrib.auth import login
from django.shortcuts import redirect
from .forms import CustomerSignUpForm

def signup(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('menu:menu_list')
    else:
        form = CustomerSignUpForm()
    return render(request, 'pages/signup.html', {'form': form})