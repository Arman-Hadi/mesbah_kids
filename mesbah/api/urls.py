from django.urls import path

from . import views


app_name = 'api'

urlpatterns = [
    path('kids', views.KidsView.as_view(), name='kids'),
    path('father', views.FatherRequestView.as_view(), name='father'),
    path('mother', views.MotherRequestView.as_view(), name='mother'),
    path('send/<slug:gender>', views.SendKidView.as_view(), name='send'),
    path('deliver/<slug:gender>', views.DeliverKidView.as_view(), name='deliver'),
    path('nezamat/<slug:gender>', views.NezamatView.as_view(), name='nezamat'),
    path('newkid', views.NewKidView.as_view(), name='newkid'),

    path('reset', views.ResetView.as_view(), name='reset'),

    path('', views.home, name='home'),
]
