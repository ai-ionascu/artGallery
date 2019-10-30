from django.conf.urls import url, include
from paintings.views import list_paintings_view, detail_paintings_view, add_painting_view


urlpatterns = [
    url(r'^$', list_paintings_view, name='paintings'),
    url( r'^(?P<id>\d+)/$', detail_paintings_view, name='painting_detail'),
    url( r'^new/$', add_painting_view, name='new_painting'),

]