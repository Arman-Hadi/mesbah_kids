from django.urls import path

from . import views


app_name = 'api'

urlpatterns = [
    path('kids', views.KidsView.as_view(), name='kids')
]
