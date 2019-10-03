from django.conf.urls import url, include
from profiles.views import login_view, logout_view, register_view, edit_profile_view, unsubscribe_view, delete_user_view
from profiles import url_reset


urlpatterns = [
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^password_reset/', include(url_reset)),
    url(r'^register/$', register_view, name='register'),
    url(r'^edit/$', edit_profile_view, name='edit_profile'),
    url(r'^unsubscribe/$', unsubscribe_view, name='unsubscribe'),
    url(r'^delete/$', delete_user_view, name='delete_profile'),

]