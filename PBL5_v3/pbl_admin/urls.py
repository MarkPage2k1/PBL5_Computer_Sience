from django.urls import path

from .views import *

urlpatterns = [
    path('', login_admin_view, name='login_admin_view'),
    path('home', list_user_view, name='home'),
    path('logout', logout_admin_view, name='logout_admin_view'),
    path('create_user', create_user_view, name='create_user'),
    path('<username>/devices', list_device_user_view, name='list_device_user'),
    path('<username>/delete', delete_user_view, name='delete_user_view'),

    path('<username>/devices/add', add_device_user_view, name='add_device_user_view'),
    path('<username>/devices/update', update_device_user_view, name='update_device_user_view'),
    path('<username>/devices/delete', delete_device_user_view, name='delete_device_user_view'),
]
