from django import forms
from .models import Match, KnockOutTeamSelection
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class CommentForm(forms.Form):
	comment = forms.SlugField(required=True, label="", widget=forms.Textarea)


class ScoreForm(forms.Form):
# *************************************** CHANGE YOUR MATCH TYPE HERE ***************************************************
	MATCH_TYPE = 'grp1' #'grp1','grp2','grp3', 'r16', 'qf', 'sf', 'f'
# ***********************************************************************************************************************

	def __init__(self, *args, **kwargs):
		m = Match.objects.filter(match_type=self.MATCH_TYPE)
		super(ScoreForm, self).__init__(*args, **kwargs)
		SCORE_REGEX = RegexValidator(r'^\d{1,2}-\d{1,2}$', 'Please enter the score in format 00-00 or 0-0')
		for each in m:
			self.fields[str(each.id)] = forms.CharField(label=each, max_length=5, validators=[SCORE_REGEX])


class KnockOutForm(forms.ModelForm):
	class Meta:
		model = KnockOutTeamSelection
		exclude = ['owner', 'qfpoints', 'sfpoints','fpoints','champpoints']
		labels = {'qf1':'Quarter Final 1',
				'qf2':'Quarter Final 2',
				'qf3':'Quarter Final 3',
				'qf4':'Quarter Final 4',
				'qf5':'Quarter Final 5',
				'qf6':'Quarter Final 6',
				'qf7':'Quarter Final 7',
				'qf8':'Quarter Final 8',
				'sf1': 'Semi Final 1',
				'sf2': 'Semi Final 2',
				'sf3': 'Semi Final 3',
				'sf4': 'Semi Final 4',
				'f1': 'Final 1',
				'f2': 'Final 2',
				'champion':'Champion'}



class AdminUpdateForm(forms.Form):
	def __init__(self, *args, **kwargs):
		m = Match.objects.all()
		super(AdminUpdateForm, self).__init__(*args, **kwargs)
		SCORE_REGEX = RegexValidator(r'^\d{1,2}-\d{1,2}$', 'Please enter the score in format 00-00 or 0-0')
		for each in m:
			self.fields[str(each.id)] = forms.CharField(label=each, max_length=5, validators=[SCORE_REGEX], required=False)


class AdminQuarterForm(forms.ModelForm):
	class Meta:
		model = KnockOutTeamSelection
		fields = ['qf1','qf2','qf3','qf4','qf5','qf6','qf7','qf8']
		labels = {'qf1':'Quarter Final 1',
				'qf2':'Quarter Final 2',
				'qf3':'Quarter Final 3',
				'qf4':'Quarter Final 4',
				'qf5':'Quarter Final 5',
				'qf6':'Quarter Final 6',
				'qf7':'Quarter Final 7',
				'qf8':'Quarter Final 8',
				}

class AdminSemiForm(forms.ModelForm):
	class Meta:
		model = KnockOutTeamSelection
		fields = ['sf1', 'sf2', 'sf3', 'sf4']
		labels = {'sf1': 'Semi Final 1',
				'sf2': 'Semi Final 2',
				'sf3': 'Semi Final 3',
				'sf4': 'Semi Final 4',
				}


class AdminFinalForm(forms.ModelForm):
	class Meta:
		model = KnockOutTeamSelection
		fields = ['f1', 'f2']
		labels = {'f1': 'Final 1',
				'f2': 'Final 2',
				}


class AdminChampionForm(forms.ModelForm):
	class Meta:
		model = KnockOutTeamSelection
		fields = ['champion']
		labels = {'champion':'Champion'}
