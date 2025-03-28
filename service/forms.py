from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import RiderProfile, ServiceBookingRecord, MechanicDetails

class EnrollRiderForm(UserCreationForm):
    class Meta:
        model = RiderProfile
        fields = ['username', 'email', 'contact_number', 'rider_address', 'password1', 'password2']

class RiderLoginForm(forms.Form):
    username = forms.CharField(label="Your Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Your Password")

class BookServiceForm(forms.ModelForm):
    class Meta:
        model = ServiceBookingRecord
        fields = ['bike_model', 'service_date', 'preferred_time']

class AssignMechanicForm(forms.ModelForm):
    mechanic_assigned = forms.ModelChoiceField(
        queryset=MechanicDetails.objects.all(),
        label="Choose Mechanic to Assign"
    )

    class Meta:
        model = ServiceBookingRecord
        fields = ['mechanic_assigned']
    
class UpdateStatusForm(forms.ModelForm):
    class Meta:
        model = ServiceBookingRecord
        fields = ['service_status']
        labels = {
            'service_status': 'Change Service Status'
        }
