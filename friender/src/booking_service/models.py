from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import FileExtensionValidator
from .validators import validate_doc_extension

SEX_CHOICES = [
    ("m", "male"),
    ("f", "female"),
]
# ROOM_TYPE_CHOICES = {
#     "s": "single",
#     "d": "double",
#     "o": "other"
# }

ROOM_TYPE_CHOICES = [
    ("s", "single"),
    ("d", "double"),
    ("o", "other")
]


# Guest
# Profile
# Booking
# Hotel
# Room
# HotelService
# BookingService
# Comment

'''
Каждый гость (Guest) может сделать несколько бронирований (Booking), но каждое бронирование принадлежит только одному гостю
У каждого гостя есть один профиль (Profile), и у каждого профиля есть только один гость
Каждое бронирование (Booking) может включать несколько дополнительных услуг (BookingService)
Каждый отель (Hotel) может иметь несколько номеров (Room)
Каждый отель (Hotel) может предоставлять несколько дополнительных услуг (HotelService)
Каждое бронирование (Booking) может включать несколько дополнительных услуг (HotelService), и каждая дополнительная услуга может быть включена в несколько бронирований
Каждый гость (Guest) может оставлять комментарии (HotelComment) к разным Hotel
'''


class Guest(models.Model):
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(validators=[
        MaxValueValidator(90),
        MinValueValidator(18)
    ])
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    email = models.EmailField(null=True)
    phone = PhoneNumberField(null=True, blank=False, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['first_name'], name='first_name_idx'),
            models.Index(fields=['last_name'], name='last_name_idx'),
            models.Index(fields=['age'], name='age_idx'),
        ]

    # Для визуалиции объекта в shell
    def __str__(self):
        return f" {self.first_name} {self.last_name}"


class HotelOwner(Guest):
    owner_exp_status = models.IntegerField(null=True)


class Profile(models.Model):
    photo = models.ImageField(
        null=True, blank=True, verbose_name="User photo", upload_to="users_photo/")
    id_card = models.IntegerField(null=True)
    serial_number = models.CharField(null=True, max_length=30)
    guest = models.OneToOneField(
        Guest, on_delete=models.CASCADE, related_name="profile")
    info = models.FileField(
        null=True, blank=True, upload_to="profile_info/",
        validators=[FileExtensionValidator(allowed_extensions=['doc']), validate_doc_extension]
    )

    def __str__(self):
        return f"profile: {self.id_card}"


class Hotel(models.Model):
    name = models.CharField(max_length=50)
    stars = models.FloatField(validators=[
        MinValueValidator(0.0), MaxValueValidator(5.0)
    ])
    address = models.CharField(max_length=80)
    city = models.CharField(max_length=30)
    phone = PhoneNumberField(null=False, blank=False, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(
        null=True, verbose_name="hotel_photo", upload_to="hotels_photo/", blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['name'], name='name_idx'),
            models.Index(fields=['stars'], name='stars_idx')
        ]

    def __str__(self):
        return f" {self.name} {self.city}"


class Room(models.Model):
    number = models.PositiveIntegerField(validators=[
        MaxValueValidator(1000),
        MinValueValidator(1)
    ])
    type = models.CharField(max_length=1, choices=ROOM_TYPE_CHOICES)
    price = models.FloatField()
    hotel = models.ForeignKey(
        Hotel, on_delete=models.SET_NULL, null=True, related_name="rooms")
    is_booked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.number}'


class HotelComment(models.Model):
    text = models.CharField(max_length=200, null=True)
    time = models.DateTimeField(auto_now_add=True)
    hotel = models.ForeignKey(
        Hotel, on_delete=models.SET_NULL, null=True, related_name="comments")
    guest = models.ForeignKey(
        Guest, on_delete=models.SET_NULL, null=True, related_name="comments")

    # def __str__(self):
    #     return f"Guest: {self.guest.first_name} ||| comments: {self.text}"


class Booking(models.Model):
    room = models.ForeignKey(
        Room, related_name='bookings', on_delete=models.CASCADE, null=True)
    details = models.CharField(max_length=200, null=True)
    check_in_date = models.DateTimeField(null=True)
    check_out_date = models.DateTimeField(null=True)
    guest = models.ForeignKey(
        Guest, on_delete=models.SET_NULL, null=True, related_name='bookings')
    hotel = models.ForeignKey(
        Hotel, on_delete=models.SET_NULL, null=True, related_name='bookings')
    hotel_services = models.ManyToManyField(
        'HotelService', related_name='bookings')

    # def __str__(self):
    #     return f"Guest: {self.guest.first_name} ||| Hotel: {self.hotel.name}"


class HotelService(models.Model):
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"Hotel: {self.hotel.name} ||| Service: {self.name}"


class BookingService(models.Model):
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name='services')
    service = models.ForeignKey(HotelService, on_delete=models.CASCADE)

    def __str__(self):
        return f"Booking id: {self.booking.id} ||| Service: {self.service.name}"


class Queue(models.Model):
    value = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.value)