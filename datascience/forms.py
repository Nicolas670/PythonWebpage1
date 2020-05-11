from django import forms
from .models import DataUpload, TextUpload


class UploadForm(forms.ModelForm):

    class Meta:
        model = DataUpload
        fields = ["title", "picture"]


class UploadTextForm(forms.ModelForm):

    class Meta:
        model = TextUpload
        fields = ["text"]



