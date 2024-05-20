from django import forms


class CheckRoomForm(forms.Form):
    room_number = forms.IntegerField()
    guest = forms.CharField(max_length=50, initial='Alice Cooper')
    hotel = forms.CharField(max_length=50, initial='Hotel_Hotel')
    # details = forms.CharField(max_length=200, initial='Default Details')
    check_in_date = forms.DateTimeField()
    check_out_date = forms.DateTimeField()
