from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
# Create your views here.

def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username exist')
                return render(request, 'register.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email taken')
                return render(request, 'register.html')
            else :
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                messages.info(request, 'User created')
                return render (request, 'register.html')

        else : 
            messages.info(request, 'Password does not match')
            return render (request, 'register.html')
    else : 
        return render(request, 'register.html')


def register1(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'register.html', context)

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None : 
            auth.login(request, user)
            messages.info(request, 'You are logged in')
            return render (request, 'login.html')

        else :
            messages.info(request, 'Invalid credentials...')
            return render (request, 'login.html')
    return render(request, 'login.html')


