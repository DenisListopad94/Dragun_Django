
from datetime import timedelta
import os
import random
import string
import django
from faker import Faker


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
fake = Faker()
from booking_service.models import Guest, Hotel, HotelComment, Profile, HotelService, Booking

def round_to_nearest_half(number: int) -> int:
    return round(number * 2) / 2


def generate_serial_number() -> str:
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    digits = ''.join(random.choices(string.digits, k=8))
    return f"{letters}{digits}"


def generate_fake_guests(num=20) -> None:
    for _ in range(num):
        first_name = fake.first_name()
        last_name = fake.last_name()
        age = random.randint(18, 80)
        sex = random.choice(['m', 'f'])
        email = fake.email()
        phone = fake.phone_number()

        Guest.objects.create(
            first_name=first_name,
            last_name=last_name,
            age=age,
            sex=sex,
            email=email,
            phone=phone
        )


def generate_fake_hotels(num=20) -> None:
    for _ in range(num):
        name = fake.company()
        stars = round_to_nearest_half(random.uniform(0.0, 5.0))
        address = fake.street_address()
        city = fake.city()
        phone = fake.phone_number()

        Hotel.objects.create(
            name=name,
            stars=stars,
            address=address,
            city=city,
            phone=phone,
        )


def generate_fake_comments(num=30) -> None:
    hotels = Hotel.objects.all()
    guests = Guest.objects.all()

    for _ in range(num):
        text = fake.text(max_nb_chars=200)
        time = fake.date_time_this_year()
        hotel = random.choice(hotels)
        guest = random.choice(guests)

        HotelComment.objects.create(
            text=text,
            time=time,
            hotel=hotel,
            guest=guest
        )


def generate_fake_profiles(num=20) -> None:
    guests = Guest.objects.all()

    for _ in range(num):
        # photo_path = os.path.join(settings.BASE_DIR, 'path', 'to', 'default', 'photo.jpg')  # Укажите путь к вашей фотографии по умолчанию
        id_card = random.randint(10000000, 99999999)
        serial_number = generate_serial_number()
        guest = random.choice(guests)

        Profile.objects.create(
            id_card=id_card,
            serial_number=serial_number,
            guest=guest
        )


def generate_fake_services(num=30) -> None:
    hotels = Hotel.objects.all()

    for _ in range(num):
        hotel = random.choice(hotels)
        name = fake.company()
        description = fake.text()

        HotelService.objects.create(
            hotel=hotel,
            name=name,
            description=description
        )


def generate_fake_bookings(num=20) -> None:
    guests = Guest.objects.all()
    hotels = Hotel.objects.all()
    hotel_services = HotelService.objects.all()

    for _ in range(num):
        details = fake.text(max_nb_chars=200)
        check_in_date = fake.date_time_this_year()
        check_out_date = check_in_date + timedelta(days=random.randint(1, 14))
        guest = random.choice(guests)
        hotel = random.choice(hotels)
        # services = random.sample(list(hotel_services), random.randint(1, 3))

        Booking.objects.create(
            details=details,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            guest=guest,
            hotel=hotel
        )


if __name__ == "__main__":
    # generate_fake_guests()
    # generate_fake_hotels()
    # generate_fake_comments()
    # generate_fake_profiles()
    # generate_fake_services()
    # generate_fake_bookings()
    pass