from django.urls import path
from .views import (DeleteBookingView, book_room_view,
                    check_room_availability_view,
                    home_view, hotel_view,
                    hotels_view, users_view)


urlpatterns = [
    path('', home_view, name='Home'),
    path('hotels', hotels_view, name='Hotels'),
    path('hotels/<str:hotel_name>', hotel_view, name='Hotel'),
    path('users', users_view, name='Users'),
    path('book/<str:hotel_name>/<int:user_id>/<int:room_number>/',
         book_room_view, name='Book Room'),
    path('check_room_availability',
         check_room_availability_view, name='Check Room'),
    path('delete_booking/<int:booking_id>/',
         DeleteBookingView.as_view(), name='Delete Booking')
    # re_path(r"^articles/(?P<year>[0-9]{4})/$", views.year_archive),
]
