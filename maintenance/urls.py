from django.urls import path
from . import views


urlpatterns = [
    path('show', views.m_show),
    path('statefailure', views.statefailure),
    path('service', views.service),
    path('servicelist', views.servicelist),
    path('breakequipmentlist', views.breakequipmentlist),
    path('edit', views.edit),
    path('save', views.save),
    path('success', views.success),
    path('search', views.search),
    path('fail', views.fail),
]