from django.conf.urls import url, include
from profiles.views import login_view, logout_view, register_view
from profiles import url_reset


urlpatterns = [
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^password_reset/', include(url_reset)),
    url(r'^register/$', register_view, name='register'),
]