# forms.py
from django import forms
from .models import AdminTask
from django.contrib.auth.models import User

class AssignTaskForm(forms.ModelForm):
    worker = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Workers'), required=True, empty_label="Select Worker")

    class Meta:
        model = AdminTask
        fields = ['status', 'notes', 'worker']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }
