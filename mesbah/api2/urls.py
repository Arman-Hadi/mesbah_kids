from django.urls import path

from . import views


app_name = 'api2'

urlpatterns = [
    path('kids', views.KidsView.as_view(), name='kids'),
    path('status', views.ChangeStatusView.as_view(), name='status'),
    
    path('boys-entry', views.BoysEntryView.as_view(), name='boys-entry'),
    path('girls-entry', views.GirlsEntryView.as_view(), name='girls-entry'),

    path('father-delivery', views.FatherDeliveryView.as_view(), name='father-delivery'),
    path('mother-delivery', views.MohterDeliveryView.as_view(), name='mother-delivery'),

]