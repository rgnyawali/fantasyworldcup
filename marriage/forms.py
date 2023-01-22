from django import forms
from .models import CurrentPlayer, Game, Player
from django.core.validators import RegexValidator
from datetime import datetime


class GameForm(forms.Form):
	def __init__(self, *args, **kwargs):
		p = CurrentPlayer.objects.all()[:5]
		super(GameForm, self).__init__(*args, **kwargs)
		POINT_VALIDATOR = RegexValidator(r'^\d{0,2}[bnlBNL]?$','Enter your point in the format 00, N, 00L, 00B')
		for each in p:
			self.fields[str(each.id)] = forms.CharField(label=each, max_length=3, validators=[POINT_VALIDATOR])


class NewGameForm(forms.Form):
	def __init__(self, *args, **kwargs):
		p = Player.objects.all()
		super(NewGameForm, self).__init__(*args, **kwargs)
		a = [each.name for each in p]
		choice_list = list(zip(a,a))
		for i in range(5):
			self.fields[str(i)] = forms.ChoiceField(label = 'Player '+ str(i+1), choices=choice_list)

class RegisterForm(forms.ModelForm):
	class Meta:
		model = Player
		fields = '__all__'
		labels = {'name':"Player's Full Name",'pic':'Upload Picture','strength':'Major Strength of Player','weakness':'Major Weakness of Player'}