from django import forms

from .models import Document

class DocumentForm(forms.ModelForm):
    # name = forms.CharField(max_length=255)
    # context = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Document
        exclude = ('slug', 'converter', 'is_deleted')