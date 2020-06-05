from django.urls import path
from . import views


urlpatterns = [
    path('show', views.t_show),
    path('equipmentlist', views.equipmentlist),
    path('kindjsj', views.kindjsj),
    path('kindsw', views.kindsw),
    path('kindwl', views.kindwl),
    path('kindhx', views.kindhx),
    path('kindjx', views.kindjx),
    path('kindqt', views.kindqt),
    path('stateable', views.stateable),
    path('stateunable', views.stateunable),
    path('statefailure', views.statefailure),
    path('service', views.service),
    path('broken', views.broken),
    path('search', views.search),
    path('myequipments', views.myequipments),
    path('main', views.main),
    path('mainupdate', views.mainupdate),
    path('applylist', views.applylist),
    path('yes', views.yes),
]