from django.shortcuts import render

def homepage_view(request):
    return render(request, 'frontend/index.html')