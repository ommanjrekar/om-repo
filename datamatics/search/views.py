from django.shortcuts import render
from .models import Employee
from django.db.models import Q
from .search import EmpIndex


def search_emp(request):
    cont = request.GET.get('term')
    if cont:
        data = Employee.objects.filter(Q(name__icontains=cont) | Q(location__icontains=cont))
    else:
        data = ""

    context = {
        'data':data,
    }

    return render(request, 'search.html', context)

def el_search(request):
    cont = request.GET.get('term')
    if cont:
        data = EmpIndex.search().query('match', name=cont)
    else:
        data = ""
    context = {
        'data':data,
    }
    return render(request, 'search.html', context)