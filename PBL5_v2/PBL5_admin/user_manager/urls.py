from django.urls import path

from .views import *

urlpatterns = [
    path('create_user', create_user_view, name='create_user'),
    path('', list_user_view, name='list_user'),
    path('<username>/devices', list_device_user_view, name = 'list_device_user')
]
