from django.shortcuts import render, reverse, get_object_or_404
from .models import Painting, Subject

# Create your views here.

def list_paintings_view(request):
    paintings_list = Painting.objects.all()
    return render(request,  'paintings_list.html', {'paintings': paintings_list})

def detail_paintings_view(request, id=None):
    painting = get_object_or_404(Painting, id=id)
    return render(request, 'painting_detail.html', {'painting': painting})