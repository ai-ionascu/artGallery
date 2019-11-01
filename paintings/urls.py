from django.conf.urls import url, include
from paintings.views import list_paintings_view, detail_paintings_view, add_painting_view, edit_painting_view, delete_painting_view


urlpatterns = [
    url(r'^$', list_paintings_view, name='paintings'),
    url(r'^filter/(?P<item>[-\w]+)/(?P<id>\d+)/$', list_paintings_view, name='filter'),
    url(r'^filter/(?P<item>[-\w]+)/(?P<string>[-\w]+)/$', list_paintings_view, name='string_filter'),
    url( r'^(?P<id>\d+)/$', detail_paintings_view, name='painting_detail'),
    url( r'^(?P<id>\d+)/edit/$', edit_painting_view, name='painting_edit'),
    url( r'^(?P<id>\d+)/delete/$', delete_painting_view, name='delete_painting'),
    url( r'^new/$', add_painting_view, name='new_painting'),

]