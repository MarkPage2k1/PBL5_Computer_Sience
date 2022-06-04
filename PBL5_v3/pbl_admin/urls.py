from django.urls import path

from .views import *

urlpatterns = [
    # Login - logout
    path('', login_admin_view, name='login_admin_view'),
    path('home', list_user_view, name='home'),
    path('logout', logout_admin_view, name='logout_admin_view'),
    
    # Manager user
    path('create_user', create_user_view, name='create_user'),
    path('<username>/devices', list_device_user_view, name='list_device_user'),
    path('<username>/delete', delete_user_view, name='delete_user_view'),
    path('<username>/devices/add', add_device_user_view, name='add_device_user_view'),
    
    # manager devices
    path('devices', list_devices_view, name='list_devices_view'),
    path('devices/add', add_devices_view, name='add_devices_view'),
    path('devices/update', update_devices_view, name='update_devices_view'),
    path('devices/deleted', delete_devices_view, name='delete_devices_view'),
]
