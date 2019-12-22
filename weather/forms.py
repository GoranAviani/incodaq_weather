from django import forms
from django.core.validators import RegexValidator

class SearchBarForm(forms.Form): #Note that it is not inheriting from forms.ModelForm
    search_bar_validator = RegexValidator(r'^[\w, ]+$', "This value may contain only letters, numbers, comma or space.")
    searchBarInput = forms.CharField(max_length=100, validators= [search_bar_validator])