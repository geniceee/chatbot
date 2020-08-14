from django import forms
from .models import *

# class DocumentForm(forms.Form):
#     docfile = forms.FileField(
#         label='Select a file',
#         help_text='max. 42 megabytes'
#     )

class DocumentForm(forms.ModelForm): 
  
    class Meta: 
        model = Document 
        fields = ['name', 'docimage'] 