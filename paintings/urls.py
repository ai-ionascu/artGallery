from django.conf.urls import url, include
from paintings.views import list_paintings_view


urlpatterns = [
    url(r'^$', list_paintings_view, name='paintings'),

]