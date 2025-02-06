from django import forms
from django.core.exceptions import ValidationError
import re
from apps.core.models import History

class HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = "__all__"
