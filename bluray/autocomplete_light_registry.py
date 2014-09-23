import autocomplete_light
from models import Movie

class MovieAutocomplete(autocomplete_light.AutocompleteModelTemplate):
    search_fields = ['^name']
    autocomplete_js_attributes = {
        'placeholder':'Search Movies',
    }
    choice_template = 'template_autocomplete/templated_choice.html'

autocomplete_light.register(Movie, MovieAutocomplete)
