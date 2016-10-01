from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Document

class DocumentForm(forms.ModelForm):
    # name = forms.CharField(max_length=255)
    # context = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Document
        fields = ('name', 'context',)
        help_texts = {
            'name': _('Some useful help text.'),
        }
