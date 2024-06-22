from django.urls import URLPattern, include, path

from .views import ( GuestApiViewSet, GuestsByServiceApiViewSet, HotelApiViewSet, HotelServiceApiViewSet, 
                     hello_world)


guests_patterns: list[URLPattern] = [
    # path('list', GuestApiView.as_view(), name='list'),
    # path('create', GuestApiView.as_view(), name='create'),
    # path('update', GuestApiView.as_view(), name='update'),
    # path('delete/<int:pk>', GuestApiView.as_view(), name='delete'),
    path('', GuestApiViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update'})),
    path('<int:pk>', GuestApiViewSet.as_view({'delete': 'destroy'})),
    path('by_hobby_list', GuestsByServiceApiViewSet.as_view(), name='service_list'),
]


services_patterns: list[URLPattern] = [
    path('list', HotelServiceApiViewSet.as_view(), name='list')
]

hotels_patterns: list[URLPattern] = [
    path('', HotelApiViewSet.as_view(), name='hotels'),
]

urlpatterns: list[URLPattern] = [
    path('some_url_example', hello_world),
    path('guests/', include((guests_patterns, 'guests'))),
    path('services/', include((services_patterns, 'services'))),
    path('hotels/', include((hotels_patterns, 'hotels'))),
]
