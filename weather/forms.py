from django import forms


class SearchBarForm(forms.Form): #Note that it is not inheriting from forms.ModelForm
    searchBarInput = forms.CharField(max_length=200)