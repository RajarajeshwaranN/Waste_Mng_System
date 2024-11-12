# forms.py
from django import forms
from .models import AdminTask

class AssignTaskForm(forms.ModelForm):
    class Meta:
        model = AdminTask
        fields = ['status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
