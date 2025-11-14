from django import forms
from .models import ContactMessage, ProgramSchedule

class ProgramScheduleForm(forms.ModelForm):
    start_time = forms.TimeField(input_formats=['%I.%M%p', '%I:%M%p', '%H:%M'])
    end_time = forms.TimeField(input_formats=['%I.%M%p', '%I:%M%p', '%H:%M'])

    class Meta:
        model = ProgramSchedule
        fields = '__all__'

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'address', 'phone', 'email', 'message']