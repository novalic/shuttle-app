from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.ProvidersViewSet.as_view({'post': 'create', 'get': 'list'}),
        name='provider-list'
    ),

    path(
        '<int:pk>/',
        views.ProvidersViewSet.as_view({'put': 'update', 'get': 'retrieve', 'delete': 'destroy'}),
        name='provider-detail'
    ),

    path(
        'service-area/',
        views.ServiceAreaViewSet.as_view({'post': 'create_service_area', 'get': 'list'}),
        name='service-area-list'
    ),

    path(
        'service-area/<int:pk>/',
        views.ServiceAreaViewSet.as_view({'put': 'update_service_area', 'get': 'retrieve', 'delete': 'destroy'}),
        name='service-area-detail'
    ),

    path(
        'service-area/point/',
        views.FindServiceAreaView.as_view({'get': 'find_service_areas'}),
        name='find-service-area'
    ),

]
