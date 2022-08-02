from django.urls import path

from . import views


app_name = 'api'

urlpatterns = [
    path('kids', views.KidsView.as_view(), name='kids'),
    path('father', views.FatherRequestView.as_view(), name='father'),
    path('mother', views.MotherRequestView.as_view(), name='mother'),
    path('deliver', views.ChangeStatusView.as_view(), name='deliver'),
    path('boys', views.BoysView.as_view(), name='boys'),
    path('girls', views.GirlsView.as_view(), name='girls'),
]
