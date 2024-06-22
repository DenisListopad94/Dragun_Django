from multiprocessing.managers import BaseManager
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view

from .renderers import CustomRenderer
from .serializers import GuestSerializer, HotelSerializer, HotelServiceSerializer
from booking_service.models import Guest, Hotel, HotelService
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from  django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import CustomPagination

# class GuestApiView(APIView):
#     renderer_classes: list[type[CustomRenderer]] = [CustomRenderer]

#     def get_object(self, id: int) -> Guest:
#         try:
#             return Guest.objects.get(id=id)
#         except Guest.DoesNotExist:
#             raise Http404

#     def get(self, request) -> Response:
#         guests: BaseManager[Guest] = Guest.objects.all()
#         serializer = GuestSerializer()
#         serialized_data = [serializer.serialize_guest(guest) for guest in guests]
#         return Response(serialized_data, status=status.HTTP_200_OK)


#     def put(self, request) -> Response:
#         guest_id: int = request.data.get('id')

#         if not guest_id:
#             return Response({"error": "no guest_id"},status=status.HTTP_404_NOT_FOUND)

#         guest: Guest = self.get_object(guest_id)
#         # guest - instance, сериализатор принимает instance и понимает, что это update 
#         serializer = GuestSerializer(guest, data=request.data)
#         if serializer.is_valid():
#             serializer.save() # вызывает метод create() в сериализаторе
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def post(self, request) -> Response:
#         guest = GuestSerializer(data=request.data)

#         if guest.is_valid():
#             guest.save() # вызывает метод update() в сериализаторе
#             return Response(guest.data, status=status.HTTP_201_CREATED)
#         return Response(guest.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk) -> Response:
#         guest: Guest = self.get_object(pk)
#         serializer = GuestSerializer()
#         serializer.delete(guest)
#         return Response({"message": "Guest deleted"})

class GuestApiViewSet(viewsets.ModelViewSet):
    renderer_classes: list[type[CustomRenderer]] = [CustomRenderer]
    serializer_class = GuestSerializer

    def get_queryset(self):
        return Guest.objects.all()
    
    def get_object(self):
        pk = self.kwargs['pk']
        print('pk', pk)
        return get_object_or_404(Guest, pk=pk)


# class HotelServiceApiView(APIView):
#     renderer_classes: list[type[CustomRenderer]] = [CustomRenderer]

#     def get(self, request) -> Response:
#         services: BaseManager[HotelService] = HotelService.objects.all()
#         serializer = HotelServiceSerializer(services, many=True)
#         return Response(serializer.data)
    
class HotelServiceApiViewSet(generics.ListAPIView):
    renderer_classes: list[type[CustomRenderer]] = [CustomRenderer]
    serializer_class = HotelServiceSerializer

    def get_queryset(self):
        return HotelService.objects.all()

# class GuestsByServiceApiView(APIView):
#     renderer_classes: list[type[CustomRenderer]] = [CustomRenderer]

#     def get(self, request) -> Response:
#         guests: BaseManager[Guest] = Guest.objects.filter(bookings__hotel_services__name='sport').distinct()
#         serializer = GuestSerializer(guests, many=True)
#         return Response(serializer.data)
        
class GuestsByServiceApiViewSet(generics.ListAPIView):
    renderer_classes: list[type[CustomRenderer]] = [CustomRenderer]
    serializer_class = GuestSerializer

    def get_queryset(self):
        return Guest.objects.filter(bookings__hotel_services__name='sport').distinct()

@api_view(['GET'])
def hello_world(_) -> Response:
    return Response({"message": "Hello, world!"})



# todo Настройка фильтрации с использованием django-filter
# вьюша с возможностью фильтрации, поиска 
# с указанием полей
class HotelApiViewSet(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    renderer_classes: list[type[CustomRenderer]] = [CustomRenderer]
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields = ['name', 'stars']
    search_fields = ['name', 'stars']
    ordering_fields = ['stars']
    pagination_class = CustomPagination

#! Посмотреть настройку базовой фильтрации с использованием стандартных фильтров DRF