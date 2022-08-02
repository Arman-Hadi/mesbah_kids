from django.urls import path

from . import views


app_name = 'api'

urlpatterns = [
    path('kids', views.KidsView.as_view(), name='kids'),
    path('father', views.FatherRequestView.as_view(), name='father'),
    path('mother', views.MotherRequestView.as_view(), name='mother'),
]
