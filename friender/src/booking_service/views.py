from typing import Optional
from django.utils import timezone
from datetime import timedelta
# from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime
from django.db.models import Q
from django.views import View
from django.http import HttpRequest, HttpResponse
from booking_service.forms import CheckRoomForm
from .models import Booking, Guest, Hotel, HotelComment, Room
from django.db import transaction
# def get_hotel_by_name(hotel_name):
#     hotel = Hotel.objects.filter(name__in=[hotel_name])
#     if hotel:
#         return hotel
#     else:
#         return None
# for hotel in hotels:
#     if hotel['name'] == hotel_name:
#         return hotel
# return None


# def home_view(request):
#     return HttpResponse('home')


def home_view(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name='home.html')


def hotels_view(request: HttpRequest) -> HttpResponse:
    # hotels = Hotel.objects.all()
    hotels = Hotel.objects.prefetch_related('comments').all()
    # hotels = Hotel.objects.prefetch_related(Prefetch('comments', queryset=HotelComment.objects.all())).all()

    # hotel_comments_dict = {}

    # for hotel in hotels:
    #     hotel_comments_dict[hotel.id] = list(hotel.comments.all())

    hotels_list = []

    # for hotel in hotels:
    #     hotels_list.append({'hotel': hotel, 'comments': hotel_comments_dict.get(hotel.id, [])})

    for hotel in hotels:
        # comments = HotelComment.objects.filter(hotel__name=hotel.name)
        # hotels_list.append({'hotel': hotel, 'comments': comments})
        hotels_list.append({'hotel': hotel, 'comments': hotel.comments.all()})

    context = {'hotels': hotels_list}

    return render(request=request, template_name='hotels.html', context=context)


def hotel_view(request: HttpRequest, hotel_name: str) -> HttpResponse:
    hotel = Hotel.objects.filter(name=hotel_name)
    comments = HotelComment.objects.filter(hotel__name=hotel_name)

    comment_list = []

    for comment in comments:
        guest_name = comment.guest.first_name
        comment_text = comment.text
        comment_list.append({'name': guest_name, 'text': comment_text})

    if hotel:
        return render(request=request, template_name='hotel.html', context={'hotel': hotel[0], 'comments': comment_list})
    else:
        return render(request=request, template_name='404.html')


def users_view(request: HttpRequest) -> HttpResponse:
    guests = Guest.objects.all()

    guests_list = []

    for guest in guests:
        bookings = Booking.objects.filter(
            guest_id=guest.id).prefetch_related('hotel_services')
        services_list = []
        for booking in bookings:
            for service in booking.hotel_services.all():
                services_list.append(service.name)
        guests_list.append({'guest': guest, 'services': services_list})

    context = {
        'guests': guests_list,
    }

    return render(request=request, template_name='users.html', context=context)


def book_room_view(request: HttpRequest, hotel_name: str, user_id: int, room_number: int) -> HttpResponse:
    context = {
        'hotel_name': hotel_name,
        'user_id': user_id,
        'room_number': room_number,
        'info': ''
    }

    try:
        hotel = Hotel.objects.get(name=hotel_name)
    except Hotel.DoesNotExist:
        context['hotel_name'] = 'Hotel is not found'
        return render(request, 'book.html', context)

    try:
        guest = Guest.objects.get(id=user_id)
    except Guest.DoesNotExist:
        context['user_id'] = 'User is not found'
        return render(request, 'book.html', context)

    try:
        room = Room.objects.get(hotel=hotel, number=room_number)
    except Room.DoesNotExist:
        context['room_number'] = 'Room is not found'
        return render(request, 'book.html', context)

    # транзакционное изменение
    with transaction.atomic():
        # проверка, есть ли актуальная бронь на данный номер в данном отеле
        # exists - проверяет наличие объектов в QuerySet, возвращает True\False
        if Booking.objects.filter(hotel=hotel, room=room).exists():
            context['info'] = f'hotel room: {str(room_number)} booked'
            return render(request, 'book.html', context)

        Booking.objects.create(
            guest=guest,
            hotel=hotel,
            room=room,
            details="Booking details from book_room_view",
            check_in_date=timezone.now(),
            check_out_date=timezone.now() + timedelta(days=7),  # +7 дней
        )
        room.is_booked = True
        room.save()
        # Room.objects.filter(number=room.number).update(is_booked=True)

    return render(request, 'book.html', context)


def render_check_room_view(request: HttpRequest, error: str = '') -> HttpResponse:
    form = CheckRoomForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'check_room_availability.html', context)


def get_guest_by_full_name(full_name: str) -> Optional[Guest]:
    first_name, last_name = full_name.split()
    return Guest.objects.get(Q(first_name=first_name) & Q(last_name=last_name))


def get_room_by_number_and_hotel(room_number: int, hotel_name: str) -> Room:
    return Room.objects.get(hotel__name=hotel_name, number=room_number)


def check_room_availability_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        check_room_form = CheckRoomForm(request.POST)
        if check_room_form.is_valid():
            room_number = int(request.POST.get('room_number'))
            hotel_name = request.POST.get('hotel')
            user_name = request.POST.get('guest')
            check_in_date = request.POST.get('check_in_date')
            check_out_date = request.POST.get('check_out_date')

            # Преобразование строк в datetime объекты
            check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d')
            check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d')

            try:
                guest = get_guest_by_full_name(user_name)
            except Guest.DoesNotExist:
                return render_check_room_view(request, error='User is not found')

            try:
                room = get_room_by_number_and_hotel(room_number, hotel_name)
            except:
                return render_check_room_view(request, error='Room is not found')

            try:
                hotel = Hotel.objects.get(name=hotel_name)
            except Hotel.DoesNotExist:
                return render_check_room_view(request, error='Hotel is not found')

            is_room_booked = Booking.objects.filter(
                hotel__name=hotel_name,
                room=room,
                check_in_date__lt=check_out_date,
                check_out_date__gt=check_in_date
            ).exists()

            if not is_room_booked:
                with transaction.atomic():
                    Booking.objects.create(
                        guest=guest,
                        hotel=hotel,
                        room=room,
                        details="Booking details from check_room_availability_view",
                        check_in_date=check_in_date,
                        check_out_date=check_out_date,
                    )
                    room.is_booked = True
                    room.save()
                return render_check_room_view(request, error='Booking successful')
            else:
                return render_check_room_view(request, error='Unavailable')
    return render_check_room_view(request, error='')


def error_404_view(request, exception):
    context = {}
    return render(request, '404.html', context)


class DeleteBookingView(View):
    template_name = 'delete_booking.html'

    def get(self, request: HttpRequest, booking_id: int) -> HttpResponse:
        context = {
            'booking_id': booking_id
        }
        try:
            with transaction.atomic():
                # select_for_update - блокировка записи бронирования
                booking = Booking.objects.select_for_update().get(id=booking_id)
                booking.delete()
                context['info'] = 'Deleted'
        except Booking.DoesNotExist:
            context['info'] = '404'
        except Exception as e:
            context['info'] = '500'

        return render(request, self.template_name, context)
