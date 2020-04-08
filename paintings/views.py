from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Painting, Subject, Trend, Media, Comment, Like
from artists.models import Artist
from checkout.models import OrderLineItem
from .forms import NewPainting, EditPainting, DeletePainting, CommentForm
from django.apps import apps
from django.db.models import Count

# Create your views here.

def list_paintings_view(request, item=None, id=None, string=''):
    item_obj = None
    if item and id and not string:
        paintings_list = Painting.objects.filter(**{item: id})
        if item != 'artist':
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
    comment_form = CommentForm()

    return render(request, 'painting_detail.html', {'painting': painting, 'form': comment_form})

@login_required
def add_painting_view(request):
    if request.method == 'POST':
        if request.user.profile.profile_type == 'ARTIST':
            painting_form = NewPainting(request.POST, request.FILES, request=request)
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
        painting_form = NewPainting(initial={'owner': request.user})

    return render(request, 'new_painting.html', 
                {'painting_form': painting_form})

@login_required        
def edit_painting_view(request, id):

    painting = get_object_or_404(Painting, id=id)
    
    if request.method == 'POST':
        if request.user.profile.profile_type == 'ARTIST' and request.user == painting.owner:
            edit_painting_form = EditPainting(request.POST, request.FILES, request=request, instance=painting)

            if edit_painting_form.is_valid(): 
                edit_painting_form.save()
                
                for f in painting._meta.get_fields():
                    if f.related_model and f.related_model is not User:
                        initial_object = edit_painting_form['{}'.format(f.name)].initial
                        print(initial_object)
                        if f.related_model is Subject:
                            for item in initial_object:
                                if item in f.related_model.objects.filter(owner=request.user, painting__isnull=True):
                                    print(item, 'has to be deleted')
                                    item.delete()
                        else:
                            if initial_object in f.related_model.objects.filter(owner=request.user, painting__isnull=True):
                                print(initial_object, 'has to be deleted')
                                initial_object.delete()

                messages.success(request,'Your painting has been successfully updated.')
            else:
                messages.error(request,"We couldn't upload your painting.")
        else:
            messages.error(request,"You are not allowed to alter this item.")
            
        return redirect(reverse('painting_detail', kwargs={'id': painting.id}))

    else:
        edit_painting_form = EditPainting(instance=painting)
    return render(request, 'edit_painting.html', {'edit_painting_form': edit_painting_form})

@login_required
def delete_painting_view(request, id):

    painting = get_object_or_404(Painting, id=id)
    
    if request.method == 'POST':
        if request.user.profile.profile_type == 'ARTIST' and request.user == painting.owner:
            
            painting.delete()
            
            for f in painting._meta.get_fields():
                if f.related_model and f.related_model is not User:
                    if f.related_model is Subject:
                        mtm=f.related_model.objects.filter(owner=request.user, painting__id=painting.id)
                        print(f.value_from_object(painting))
                        for m in mtm:
                            if not Painting.objects.filter(**{'{}'.format(f.name):m}):
                                print(m, 'to be deleted')
                                print(not Painting.objects.filter(**{'{}'.format(f.name):m}))
                                m.delete()
                    elif f.related_model is not OrderLineItem:
                        fk=f.related_model.objects.filter(owner=request.user, painting__id=painting.id)
                        if not Painting.objects.filter(**{'{}_id'.format(f.name):fk}):
                            print(fk, 'to be deleted')
                            print(not Painting.objects.filter(**{'{}_id'.format(f.name):fk}))
                            fk.delete()

            messages.success(request, "We have successfully deleted your painting.")
            return redirect(reverse('paintings'))
        else:
            messages.error(request, "You are not allowed to delete this item.")
          
    return render(request, 'delete_painting.html', {'painting': painting})

def add_comment_view(request, id):
        painting = get_object_or_404(Painting, id=id)
        if request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.painting = painting
                comment.user = request.user
                comment.save()
                print('pula mea')
        return redirect(reverse('painting_detail', kwargs={'id':painting.id}))

def like_painting_view(request, id):
    painting = get_object_or_404(Painting, id=id)

    try:
        painting.likes
    except Painting.likes.RelatedObjectDoesNotExist:
        Like.objects.create(painting=painting)

    if request.user in painting.likes.users.all():
        painting.likes.users.remove(request.user)
    else:
        painting.likes.users.add(request.user)
    return redirect(reverse('painting_detail', kwargs={'id':painting.id}))
