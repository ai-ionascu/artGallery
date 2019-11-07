from django.shortcuts import render, reverse, redirect, get_object_or_404
from paintings.models import Artist

# Create your views here.

def list_artists_view(request):
         
    artists_list = Artist.objects.all().order_by('name')
    return render(request, 'artists_list.html', {'artists': artists_list})

def detail_artist_view(request, id=None):
    artist = get_object_or_404(Artist, id=id)
    return render(request, 'artist_detail.html', {'artist': artist})