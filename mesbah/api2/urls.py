from django.urls import path

from . import views


app_name = 'api2'

urlpatterns = [
    path('addkid', views.AddKidView.as_view(), name='addkid'),
    path('kids', views.KidsView.as_view(), name='kids'),
    path('status', views.ChangeStatusView.as_view(), name='status'),
    path('undo', views.UndoStatusView.as_view(), name='undo'),

    path('<slug:kids>-entry', views.KidsEntryView.as_view(), name='kids-entry'),

    path('<slug:parent>-delivery', views.ParentDeliveryView.as_view(), name='parent-delivery'),

    path('porsline', views.GetPorslineData.as_view(), name='porsline'),

    path('token', views.CreateAuthToken.as_view(), name='token')
]
