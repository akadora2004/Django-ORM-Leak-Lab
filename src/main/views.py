from django.shortcuts import render
from .models import Employee
# Create your views here.



def index(request):

    query_params = request.GET.dict()

    results = Employee.objects.filter(**query_params)

    return render(request, 'main/index.html', {
        'results': results,
        })

def safe(request):
    name = request.GET.get('name')
    dept = request.GET.get('department')

    results2 = Employee.objects.all()
    if name:
        results2 = results2.filter(name=name)
    if dept:
        results2 = results2.filter(department=dept)

    return render(request, 'main/safe.html', {
        'results2': results2,
    })