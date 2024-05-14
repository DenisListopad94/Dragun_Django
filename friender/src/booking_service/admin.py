from django.contrib import admin
from django.utils.html import format_html
from .models import Booking, BookingService, Guest, Hotel, HotelComment, HotelService, Profile, Room


class AgeFilter(admin.SimpleListFilter):
    title = 'Age'
    parameter_name = 'age'

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            age_range_start = int(value)
            age_range_end = age_range_start + 9
            return queryset.filter(age__range=(age_range_start, age_range_end))
        else:
            return queryset
        
    def lookups(self, request, model_admin):
        return (
            ('10', '10s'),
            ('20', '20s'),
            ('30', '30s'),
            ('40', '40s'),
            ('50', '50s'),
            ('60', '60s'),
            ('70', '70s'),
            ('80', '80s'),
        )

'''
TabularInline,
StackedInline,
AdminTabularInline,
AdminStackedInline
'''

class HotelCommentInline(admin.TabularInline):
    model = HotelComment
    extra = 0 

class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0

class RoomInline(admin.TabularInline):
    model = Room
    extra = 0

class GuestAdmin(admin.ModelAdmin):
    inlines = [BookingInline]
    list_display = ['first_name', 'last_name', 'age', 'sex', 'email', 'phone'] #отображение полей в общем списке
    search_fields = ['first_name', 'age'] # поисковая строка
    list_filter = [AgeFilter, 'sex'] # отображения фильтра рядом с таблицей
    list_editable = ['age'] #редактирование поля в общем списке
    fieldsets = ( #раздение информации по темам
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'age', 'sex')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone'),
            'classes': ('collapse',)  # блок по умолчанию скрыт
        }),
    )
    # actions = [
    #     highlight_selected_fields,
    # ]

class HotelAdmin(admin.ModelAdmin):
    inlines = [HotelCommentInline, BookingInline, RoomInline]
    list_display = ['name', 'stars', 'address', 'city', 'phone']
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'stars')
        }),
        ('Contact Information', {
            'fields': ('city', 'address', 'phone')
        }),
    )

class HotelCommentAdmin(admin.ModelAdmin):
    list_display = ['get_guest_name', 'get_hotel_name', 'strikethrough_comment_text', 'time']

    def get_guest_name(self, obj): #получение имя клиента (Fk)
        guest = obj.guest
        if guest:
            return guest.first_name
        return None
    get_guest_name.short_description = 'Guest' # кастомный заголовок

    def get_hotel_name(self, obj): 
        hotel = obj.hotel
        if hotel:
            return hotel.name
        return None
    get_hotel_name.short_description = 'Hotel'

    def strikethrough_comment_text(self, obj):
        guest = obj.guest
        if guest:
            return obj.text
        return format_html('<p style="color: red;"><strike>{}</strike></p>', obj.text)
    strikethrough_comment_text.short_description = 'Comment'


# @admin.action(description="TEST")
# def highlight_selected_fields(modeladmin, request, queryset):
#     selected_fields = queryset.values_list('id', flat=True)
#     print("Selected fields:", list(selected_fields))

admin.site.register(Guest, GuestAdmin)
admin.site.register(Profile)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(Room)
admin.site.register(HotelComment, HotelCommentAdmin)
admin.site.register(Booking)
admin.site.register(HotelService)
admin.site.register(BookingService)
