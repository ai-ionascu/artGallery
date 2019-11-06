from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Painting, Artist, Subject, Trend, Media
from .forms import NewPainting, EditPainting, DeletePainting
from django.apps import apps
from django.db.models import Count

# Create your views here.

def list_paintings_view(request, item=None, id=None, string=''):
    item_obj = None
    if item and id and not string:
        paintings_list = Painting.objects.filter(**{item: id})
        model = apps.get_model('paintings', item.capitalize())
        item_obj = model.objects.get(id=id)
        if paintings_list.count() is 0:
            messages.error(request, "Our gallery doesn't have any item of the selected type.")
    elif item and not id and string:
        if string == 'all':
            if item != 'size':
                model = apps.get_model('paintings', item.capitalize())
                item_obj = model.objects.all().annotate(counter=Count('painting__{}'.format(item))).order_by('-counter')
            else:
                item_obj =[i[0] for i in Painting._meta.get_field('{}'.format(item)).choices if i[0]]
 
            paintings_list =[{i:Painting.objects.filter(**{item:i})} for i in item_obj]
        else:
            paintings_list = Painting.objects.filter(**{item: string.upper()})  
            if paintings_list.count() is 0:
                messages.error(request, "Our apologies, we don't have items in this size.")
    else:        
        paintings_list = Painting.objects.all()
    return render(request,  'paintings_list.html', {'paintings': paintings_list, 'item_obj': item_obj, 'item': item, 'id': id, 'string': string})

def detail_paintings_view(request, id=None):
    painting = get_object_or_404(Painting, id=id)
    return render(request, 'painting_detail.html', {'painting': painting})

@login_required
def add_painting_view(request):
    if request.method == 'POST':
        if request.user.profile.profile_type == 'ARTIST':
            painting_form = NewPainting(request.POST, request.FILES)
            if painting_form.is_valid():
                painting_form.save()
                messages.success(request,'Your painting has been successfully uploaded.')
                return redirect(reverse('paintings'))
            else:
                messages.error(request,"We couldn't upload your painting.")
        else:
            messages.error(request,"Don't try to cheat, please register as an artist.")
            return redirect(reverse('register'))
    else:
        painting_form = NewPainting(initial={'artist_user': request.user})

    return render(request, 'new_painting.html', 
                {'painting_form': painting_form})

@login_required        
def edit_painting_view(request, id):

    painting = get_object_or_404(Painting, id=id)
    
    if request.method == 'POST':
        if request.user.profile.profile_type == 'ARTIST' and request.user == painting.artist_user:
            edit_painting_form = EditPainting(request.POST, request.FILES, instance=painting)
            if edit_painting_form.is_valid():
                edit_painting_form.save()
                messages.success(request,'Your painting has been successfully updated.')
            else:
                messages.error(request,"We couldn't upload your painting.")
        else:
            messages.error(request,"You are not allowed to alter this item.")
            
        return redirect(reverse('painting_detail', kwargs={'id': painting.id}))

    else:
        edit_painting_form = EditPainting(instance=painting,
                                        initial={'artist': painting.artist,
                                                'trend': painting.trend,
                                                'media': painting.media,
                                                'subject': [i for i in Subject.objects.filter(painting__id=id)]})

    return render(request, 'edit_painting.html', {'edit_painting_form': edit_painting_form})

@login_required
def delete_painting_view(request, id):

    painting = get_object_or_404(Painting, id=id)

    if request.method == 'POST':
        if request.user.profile.profile_type == 'ARTIST' and request.user == painting.artist_user:
            del_painting = Painting.objects.get(id=painting.id)
            del_painting.delete()
            messages.success(request, "We have successfully deleted your painting.")
            return redirect(reverse('paintings'))
        else:
            messages.error(request, "You are not allowed to delete this item.")

    return render(request, 'delete_painting.html')