from django import forms
from django.core.validators import validate_slug

class SearchBarForm(forms.Form): #Note that it is not inheriting from forms.ModelForm
    searchBarInput = forms.CharField(max_length=200, validators= [validate_slug])