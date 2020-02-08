from django.urls import path
from api.views import login_view,register_view,logout_view,home

from django.conf.urls import url


urlpatterns = [
    
    path('', home),
    path('accounts/login/', login_view),
    path('accounts/register/', register_view),
    path('accounts/logout/', logout_view)
]

