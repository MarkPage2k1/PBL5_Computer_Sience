from django.urls import path

from .views import *


urlpatterns = [
    path('', login_view, name='login'),
    path('home', home_view, name='home'),
    path('logout', logout_view, name='logout_view'),
    path('changepass', change_pass_view, name='change_pass_view'),
    path('control', control_view, name='control'),
]
