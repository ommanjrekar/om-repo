from .models import Employee
from django.shortcuts import render, redirect
from django.db.models import Q


def dashboard(request):
    if request.method == 'POST': # If the form is submitted
        search_query = request.POST['search_box']
        try:
            resp = Employee.objects.filter(Q(edu__iexact=search_query) | Q(name__icontains=search_query) | Q(loc__iexact=search_query))
            emp = Employee.objects.all()
        except:
            resp = ''
        context = {
            'resp' : resp,
            'emp' : emp
        }
        return render(request, 'templates/dashboard.html', context)
    else :
        try:
            emp = Employee.objects.all()
        except:
            emp = ''
        resp = ''
        context = {
            'resp' : resp,
            'emp' : emp
        }
        return render(request, 'templates/dashboard.html', context)

def goto_dash(request):
    return render(request, 'templates/home.html')
