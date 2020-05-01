from django import forms
from .models import DataUpload


class UploadForm(forms.ModelForm):

    class Meta:
        model = DataUpload
        fields = ["title", "picture"]