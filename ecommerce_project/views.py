from django.shortcuts import render

def home(request):
    return render(request, 'home.html')  # Template for the home page
