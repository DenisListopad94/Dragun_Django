from multiprocessing.managers import BaseManager
from typing import Optional
from django.utils import timezone
from datetime import timedelta
# from django.http import JsonResponse
from django.shortcuts import redirect, render
from datetime import datetime
from django.db.models import Q
from django.views import View
from django.http import HttpRequest, HttpResponse
from .forms import AddCommentForm, AddGuestForm, AddGuestForm2, CheckRoomForm
from .models import Booking, Guest, Hotel, HotelComment, Room
from django.db import transaction
from django.views.generic import TemplateView
from django.views.generic import CreateView, FormView
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required, permission_required


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


# def home_view(request: HttpRequest) -> HttpResponse:
#     return render(request=request, template_name='home.html')
'''
TemplateView - класс представления для отображения шаблонов без данных из бд
'''
class HomeView(TemplateView):
    template_name: str = 'home.html'

#* login_required - доступ только для аутентифицированных в админке
#* permission_requiered - доступ только с правами для просмотра в админке
@permission_required("booking_service.hotels_view",login_url="/admin/login/")
@login_required(login_url="/admin/login/")
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
    hotel: BaseManager[Hotel] = Hotel.objects.filter(name=hotel_name).first()

    if not hotel:
        return render(request=request, template_name='404.html')

    comments: BaseManager[HotelComment] = HotelComment.objects.filter(hotel__name=hotel_name)
    comment_list: list = []

    if request.method == 'POST':
        comment_form = AddCommentForm(request.POST)
        if comment_form.is_valid():
            # костыль, предполагаем, что зарег пользователь в бд оставляет коммент
            guest: Guest = Guest.objects.get(first_name='Jacob', last_name = 'Collins')
            '''
            commit=True по умолчанию, сохраняет изменения в базу данных и возвращает экземпляр модели
            commit=False создает объект модели и заполняет его данными из формы, но не сохраняет его в базу данных.
            позволяет изменить данные перед сохранением
            '''
            new_comment = comment_form.save(commit=False)
            new_comment.guest = guest
            new_comment.hotel = hotel
            new_comment.save()

            return redirect('hotel', hotel_name=hotel_name)
    else:
        comment_form = AddCommentForm()

    for comment in comments:
        guest_name: str | None = comment.guest.first_name
        comment_text: str | None = comment.text
        comment_list.append({'name': guest_name, 'text': comment_text})

    context = {'hotel': hotel, 'comments': comment_list, 'comment_form': comment_form}
    return render(request=request, template_name='hotel.html', context=context)


class GuestListView(ListView):
    model = Guest
    template_name = 'guest_list.html' 
    context_object_name = 'guests'
    paginate_by = 3 

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
        #* проверка, есть ли актуальная бронь на данный номер в данном отеле
        #* exists - проверяет наличие объектов в QuerySet, возвращает True\False
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
                guest: Guest | None = get_guest_by_full_name(user_name)
            except Guest.DoesNotExist:
                return render_check_room_view(request, error='User is not found')

            try:
                room: Room = get_room_by_number_and_hotel(room_number, hotel_name)
            except:
                return render_check_room_view(request, error='Room is not found')

            try:
                hotel: Hotel = Hotel.objects.get(name=hotel_name)
            except Hotel.DoesNotExist:
                return render_check_room_view(request, error='Hotel is not found')

            is_room_booked: bool = Booking.objects.filter(
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


def error_404_view(request, exception) -> HttpResponse:
    return render(request, '404.html', {})


class DeleteBookingView(View):
    template_name: str = 'delete_booking.html'

    def get(self, request: HttpRequest, booking_id: int) -> HttpResponse:
        context: dict[str, int] = {
            'booking_id': booking_id
        }
        try:
            with transaction.atomic():
                #* select_for_update - блокировка записи бронирования
                booking: Booking = Booking.objects.select_for_update().get(id=booking_id)
                booking.delete()
                context['info'] = 'Deleted'
        except Booking.DoesNotExist:
            context['info'] = '404'
        except Exception as e:
            context['info'] = '500'

        return render(request, self.template_name, context)


#* вьюшка для добавления гостя через класс CreateView. Форма связана с моделью Guest
# class AddGuestView(CreateView):
#     model = Guest
#     form_class = AddGuestForm2
#     template_name = 'add_guest.html'
#     success_url = reverse_lazy('guest_list')

#* вьюшка для добавления гостя через класс FormView. Форма НЕ связана с моделью Guest
class AddGuestView(FormView):
    form_class = AddGuestForm
    template_name = 'add_guest.html'
    success_url = reverse_lazy('guest_list') 

    def form_valid(self, form) -> HttpResponse:
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        age = form.cleaned_data['age']
        sex = form.cleaned_data['sex']
        email = form.cleaned_data['email']
        phone = form.cleaned_data['phone']
        
        Guest.objects.create(first_name=first_name, last_name=last_name, age=age, sex=sex, email=email, phone=phone)
        
        return super().form_valid(form)


#* Рабочий вариант через класс View
# class AddGuestView(View):
#     template_name: str = 'add_guest.html'

#     def get(self, request: HttpRequest) -> HttpResponse:
#         form = AddGuestForm() #пустой экземпляр формы
#         return render(request, self.template_name, {'form':form})

#     def post(self, request: HttpRequest) -> HttpResponse:
#         form = AddGuestForm(request.POST)
#         if form.is_valid():
#             form.save() # Сохранение формы в бд
#             return redirect('Users')
#         return render(request, self.template_name, {'form':form})
    

class GuestDeleteView(DeleteView):
    model = Guest
    template_name = 'guest_confirm_delete.html'
    success_url = reverse_lazy('guest_list')

