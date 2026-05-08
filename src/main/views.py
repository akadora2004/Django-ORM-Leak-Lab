from django.shortcuts import render
from .models import Employee
# Create your views here.



def index(request):

    query_params = request.GET.dict()

    results = Employee.objects.filter(**query_params)

    return render(request, 'main/index.html', {
        'results': results,
    })