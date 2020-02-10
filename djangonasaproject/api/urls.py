from django.urls import path
from api.views import login_view,register_view,logout_view,home,search_view

from django.conf.urls import url


urlpatterns = [
    
    path('', home),
    path('accounts/login/', login_view,name='login'),
    path('accounts/register/', register_view,name='register'),
    path('accounts/logout/', logout_view),
    path('library/',search_view)
]

