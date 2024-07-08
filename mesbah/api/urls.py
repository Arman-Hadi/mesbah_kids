from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views


app_name = 'api'

protected_urls = [
    ('send/<slug:gender>', views.SendKidView.as_view(), 'send'),
    ('deliver/<slug:gender>', views.DeliverKidView.as_view(), 'deliver'),
    ('reset', views.ResetView.as_view(), 'reset')
]

urlpatterns = [
    path(i[0], login_required(i[1], login_url='admin:login'), name=i[2])
    for i in protected_urls
]

urlpatterns += [
    path('logout', views.logout_view, name='logout'),
    path('status', views.ChangeStatusView.as_view(), name='status'),
    path('kids', views.KidsView.as_view(), name='kids'),
    path('father', views.FatherRequestView.as_view(), name='father'),
    path('mother', views.MotherRequestView.as_view(), name='mother'),
    # path('send/<slug:gender>', views.SendKidView.as_view(), name='send'),
    # path('deliver/<slug:gender>', views.DeliverKidView.as_view(), name='deliver'),
    # path('nezamat/<slug:gender>', views.NezamatView.as_view(), name='nezamat'),
    path('nezamat', views.NezamatView.as_view(), name='nezamat'),
    path('newkid', views.NewKidView.as_view(), name='newkid'),
    path('numbers', views.NumbersView.as_view(), name='numbers'),

    # path('reset', views.ResetView.as_view(), name='reset'),

    path('', views.home, name='home'),
]
