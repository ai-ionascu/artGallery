from django.conf.urls import url, include
from artists.views import list_artists_view, detail_artist_view


urlpatterns = [
    url(r'^$', list_artists_view, name='artists'),
    url( r'^(?P<id>\d+)/$', detail_artist_view, name='artist_detail'),

]