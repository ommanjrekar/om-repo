from django.shortcuts import render,redirect
from django.contrib.auth.models  import User,auth
from django.contrib import messages
import datetime
from django.conf import settings

def home(request):
    return render(request,'home.html')

def my_view(request):
    context = {
        'api_key': settings.API_KEY
    }
    return render('index.html', context)

def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Invalid credentials')
            return redirect('login')

    else:
        return render(request,'login.html')


def register(request):
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']
        email=request.POST['email']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username already exists!')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email already taken')
                return redirect('register')
            else:
                user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=password1,email=email)
                user.save()
                messages.info(request,"User created")
                return redirect('login')
                
        else:
            messages.info(request,'Password not matching')
            return redirect('register')
        return redirect('/')

    else:
        return render(request,'register.html')

def contact(request):
    return render(request,'contact.html')

def between(request):
    return render(request,'between.html')

def tz(request):
    now = datetime.datetime.now()
    return render(request,'/',{'time':now})

def subscribe(request):
    return render(request,'/')



def logout(request):
    auth.logout(request)
    return redirect('/')

