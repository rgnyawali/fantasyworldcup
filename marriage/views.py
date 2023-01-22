from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import GameForm, NewGameForm, RegisterForm
from .models import CurrentPlayer, Player, Game
from django.urls import reverse
from django.db.models import Sum


# Create your views here.

def indexview(request):
	msg = "Hello"
	players = CurrentPlayer.objects.count()
	context = {'players':players}
	return render(request, 'marriage/index.html', context)

class NewPlayerView(View):
	def get(self, request):
		registerform = RegisterForm()
		context = {'registerform':registerform}
		return render(request, 'marriage/newplayer.html', context)

	def post(self, request):
		registerform=RegisterForm(request.POST)
		if registerform.is_valid():
			registerform.save()

		return redirect(reverse('marriage:newgame'))


class NewGameView(View):
	def get(self, request):
		newgameform = NewGameForm()
		context = {'form':newgameform}
		return render(request, 'marriage/newgame.html', context)

	def post(self, request):
		newgameform = NewGameForm(request.POST)
		if newgameform.is_valid():
			CurrentPlayer.objects.all().delete()
			Game.objects.all().delete()
			for key,value in newgameform.cleaned_data.items():
				if not value == 'X':
					cp = CurrentPlayer(name=value)
					cp.save()
				
		return redirect(reverse('marriage:gameroom'))

class GameView(View):
	def get(self, request):

		gameform = GameForm()
		game_data=Game.objects.all()
		current_player=CurrentPlayer.objects.all()
		n=CurrentPlayer.objects.count()
		summary = list(Game.objects.aggregate(Sum('s0'),Sum('s1'),Sum('s2'),Sum('s3'),Sum('s4')).values())[:n]
		context = {'form':gameform, 'game_data':game_data,'current_player':current_player,'summary':summary}
		return render(request, 'marriage/gameplay.html',context)

	def post(self, request):
		gameform = GameForm(request.POST)
		if gameform.is_valid():
			raw_data = list(gameform.cleaned_data.values())
			if self.verify_values(raw_data):
				final_point=self.calculate(raw_data)
				g = Game()
				g.save()
				try:
					g.r0=raw_data[0]
					g.s0=final_point[0]
				except:
					pass
				try:
					g.r1=raw_data[1]
					g.s1=final_point[1]
				except:
					pass 
				try:
					g.r2=raw_data[2]
					g.s2=final_point[2]
				except:
					pass 
				try:
					g.r3=raw_data[3]
					g.s3=final_point[3]
				except:
					pass 
				try:
					g.r4=raw_data[4]
					g.s4=final_point[4]
				except:
					pass
				g.save()
				return redirect(reverse('marriage:gameroom'))
			else:
				msg = 'Error! Select one (and only one) winner for this hand.'

		else:
			msg = 'Error! The values were not valid. Please check again.'

		game_data = Game.objects.all()
		current_player = CurrentPlayer.objects.all()
		context = {'msg':msg, 'form':gameform, 'game_data':game_data, 'current_player':current_player}
		return render(request, 'marriage/gameplay.html', context)

	def verify_values(self, raw_data):
		b = 0
		for each in raw_data:
			if ('b' in each) or ('B' in each): b+=1
		return(b==1)

	def calculate(self, raw_data):
		total_maal=0
		less_pt=0
		not_seen=0
		seen=0
		n_player=len(raw_data)
		return_list=[]
		for each in raw_data:
			data=self.get_point(each)
			total_maal+=data[0]
			if data[1]=='S': seen+=1
			if data[1]=='L': less_pt+=1
			if data[1]=='N': not_seen+=1
# Here is some repetition, that needs to be addressed.
		for each in raw_data:
			data=self.get_point(each)
			if data[1]=='S': return_list.append(data[0]*n_player-total_maal-3)
			if data[1]=='L': return_list.append(data[0]*n_player-total_maal)
			if data[1]=='N': return_list.append(-total_maal-10)
			if data[1]=='B': return_list.append(data[0]*n_player-total_maal+not_seen*10+seen*3)
		return(return_list)

	def get_point(self, str):
		if str.isdigit(): return (int(str),'S')
		if ('l' in str) or ('L' in str):
			a = str.replace('l','')
			a = a.replace('L','')
			if a=='': a='0'
			return (int(a),'L')
		if ('n' in str) or ('N' in str): return (0,'N')
		if ('b' in str) or ('B' in str):
			a = str.replace('b','')
			a = a.replace('B','')
			if a=='': a='0'
			return (int(a),'B')
		return ()




