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

    results2 = Employee.objects.all()
    if name:
        results2 = results2.filter(name=name)

    return render(request, 'main/safe.html', {
        'results2': results2,
    })
