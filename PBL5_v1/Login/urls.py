from django.urls import path

from Login.views import login_view, reghister_view
urlpatterns = [
    path('', login_view, name = 'login'),
    path('reghister', reghister_view, name = 'reghister')
]
