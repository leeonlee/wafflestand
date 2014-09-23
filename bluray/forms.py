from django import forms
import autocomplete_light

from models import Movie

class SearchForm(forms.Form):
    movie = forms.ModelChoiceField(Movie.objects.all(), widget = autocomplete_light.ChoiceWidget('MovieAutocomplete'))

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['movie'].widget.attrs.update({'class':'form-control'})
