from django.urls import path

from . import views


app_name = 'api2'

urlpatterns = [
    path('kids', views.KidsView.as_view(), name='kids'),
    path('status', views.ChangeStatusView.as_view(), name='status'),
]
