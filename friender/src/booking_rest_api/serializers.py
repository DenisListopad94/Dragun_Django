from multiprocessing.managers import BaseManager
from rest_framework import serializers
from django.core.validators import MaxValueValidator, MinValueValidator

from booking_service.models import SEX_CHOICES, Guest, Hotel, HotelService

#* сериализатор для модели Guest (не связан с моделью)
class GuestSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30, allow_null=True)
    last_name = serializers.CharField(max_length=50)
    age = serializers.IntegerField(validators=[
        MaxValueValidator(90),
        MinValueValidator(18)
    ])
    sex = serializers.ChoiceField(choices=SEX_CHOICES)
    email = serializers.EmailField(required=False, allow_null=True)
    phone = serializers.CharField(required=False, allow_blank=False, allow_null=True)

    def serialize_guest(self, instance):# -> dict[str, Any]:
       return {
            'id': instance.id,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'age': instance.age,
            'sex': instance.sex,
            'email': instance.email,
            'phone': str(instance.phone)
        }

    def create(self, validated_data) -> Guest:
        return Guest.objects.create(**validated_data)
    
    def update(self, instance, validated_data) -> Guest:
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.age = validated_data.get('age', instance.age)
        instance.sex = validated_data.get('sex', instance.sex)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance
    
    def delete(self, instance) -> None:
        instance.delete()

#* сериализатор для модели HotelService (связан с моделью)
class HotelServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelService
        fields: list[str] = ['id', 'name', 'description']


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'