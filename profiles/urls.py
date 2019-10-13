from django.conf.urls import url, include
from profiles.views import login_view, logout_view, registration_view, new_profile_view, edit_profile_view, unsubscribe_view, delete_user_view, reactivate_subscription_view
from profiles import url_reset


urlpatterns = [
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^password_reset/', include(url_reset)),
    url(r'^register/$', registration_view, name='register'),
    url(r'^new/profile/$', new_profile_view, name='new_profile'),
    url(r'^edit/$', edit_profile_view, name='edit_profile'),
    url(r'^unsubscribe/$', unsubscribe_view, name='unsubscribe'),
    url(r'^subscription/reactivate/$', reactivate_subscription_view, name='resubscribe'),
    url(r'^delete/$', delete_user_view, name='delete_profile'),

]