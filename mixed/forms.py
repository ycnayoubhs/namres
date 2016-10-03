from django import forms
from django.contrib.auth.forms import AuthenticationForm as NativeAuthenticationForm
from django.utils.translation import ugettext_lazy as _

from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('name', 'context',)
        help_texts = {
            'name': _('Some useful help text.'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Document Name'}),
            'context': forms.Textarea(attrs={'placeholder': 'Document Context'}),
        }


class AuthenticationForm(NativeAuthenticationForm):
    # username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    # password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control',
            'placeholder': 'Username',
        })
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control',
            'placeholder': 'Password',
        })
