from django import forms

class NombreMesForm(forms.Form):
    nombre_mes = forms.CharField(label='Nombre del mes', max_length=100)

class CountryNameForm(forms.Form):
	country_name = forms.CharField(label='Country name', max_length=255)

class PlayerNameForm(forms.Form):
	player_name = forms.CharField(label='Player name', max_length=255)
	player_last_name = forms.CharField(label='Last name', max_length=255)

class SearchForm(forms.Form):
	search_str = forms.CharField(label='Search player', max_length=255)