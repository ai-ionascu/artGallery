from django.shortcuts import render

# Create your views here.

def index_view(request):
    # returns the gallery homepage
    
    return render(request, 'index.html')