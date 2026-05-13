# attendance/forms.py
from django import forms
from .models import Attendance   # model import karna zaroori hai

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance       # yahan model specify karna hoga
        fields = ['employee', 'date', 'status']
