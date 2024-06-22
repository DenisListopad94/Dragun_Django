from django.urls import URLPattern, path
from .views import (DeleteBookingView, AddGuestView, GuestDeleteView, GuestListView, book_room_view,
                    check_room_availability_view,
                    HomeView, custom_login_view, custom_logout_view, custom_register_view, hotel_view,
                    hotels_view, users_view)


urlpatterns: list[URLPattern] = [
    #  path('', home_view, name='home'),
    path('', HomeView.as_view(), name='home'),
    path('hotels', hotels_view, name='hotels'),
    path('hotels/<str:hotel_name>', hotel_view, name='hotel'),
    path('users', users_view, name='guest_list'),
    path('book/<str:hotel_name>/<int:user_id>/<int:room_number>/',
         book_room_view, name='book_room'),
    path('check_room_availability',
         check_room_availability_view, name='check_room'),
    path('delete_booking/<int:booking_id>/',
         DeleteBookingView.as_view(), name='delete_Booking'),
    path('add_guest', AddGuestView.as_view(), name='add_guest'),
    path('guest/<int:pk>/delete', GuestDeleteView.as_view(), name='guest_delete'),
    path('guests', GuestListView.as_view(), name='guest_list'),
    # re_path(r"^articles/(?P<year>[0-9]{4})/$", views.year_archive),

    path('register', custom_register_view, name='register'),
    path('login', custom_login_view, name='login'),
    path('logout', custom_logout_view, name='logout'),
]
