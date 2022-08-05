from django.urls import path

from . import views


app_name = 'api'

urlpatterns = [
    path('kids', views.KidsView.as_view(), name='kids'),
    path('father', views.FatherRequestView.as_view(), name='father'),
    path('mother', views.MotherRequestView.as_view(), name='mother'),
    path('deliver', views.ChangeStatusView.as_view(), name='deliver'),
    path('send/<slug:gender>', views.SendKidView.as_view(), name='send'),
    path('newkid', views.NewKidView.as_view(), name='newkid'),

    path('reset', views.ResetView.as_view(), name='reset'),
]
