from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Player, Match
from .forms import AdminForm

# Create your views here.
class HomeView(View):
    players = Player.objects.all().order_by('-won','played','name')
    matches = Match.objects.all().order_by('-id')
    def get(self, request):
        context={'players':self.players, 'matches':self.matches}
        return render(request, 'tt/home.html',context)

class MatchDetailView(View):
    def get(self, request):
        context={'yes':'yes'}
        return render(request, 'tt/report.html',context)

class TrialView(View):
    players = Player.objects.all().order_by('-won','played','name')
    matches = Match.objects.all().order_by('id')
    def get(self, request):
        context={'players':self.players, 'matches':self.matches}
        return render(request, 'tt/trial.html',context)

class AdminView(LoginRequiredMixin, View):
    def get (self, request):
        if request.user.is_superuser:
            adform = AdminForm()
            context = {'form':adform, 'is_superuser':request.user.is_superuser}
            return render(request, 'tt/admin.html', context)
        else:
            context = {'is_superuser':request.user.is_superuser}
            return render(request, 'tt/admin.html',context)

    def post(self, request):
        adform = AdminForm(request.POST)
        players = Player.objects.all()
        if adform.is_valid():
            data = adform.cleaned_data
            win1 = 0
            win2 = 0
            score1 = data['score1']
            score2 = data['score2']
            score3 = data['score3']
            score4 = data['score4']
            score5 = data['score5']
            if score1 != None:
                p1s1 = int(score1.split('-')[0])
                p2s1 = int(score1.split('-')[1])
                if p1s1 > p2s1:
                    win1 += 1
                else:
                    win2 += 1
            else:
                p1s1=None
                p2s1=None

            if score2 != None:
                p1s2 = int(score2.split('-')[0])
                p2s2 = int(score2.split('-')[1])
                if p1s2 > p2s2:
                    win1 += 1
                else:
                    win2 += 1
            else:
                p1s2 = None
                p2s2=None

            if score3 != None:
                p1s3 = int(score3.split('-')[0])
                p2s3 = int(score3.split('-')[1])
                if p1s3 > p2s3:
                    win1 += 1
                else:
                    win2 += 1
            else:
                p1s3=None
                p2s3=None

            if score4 != None:
                p1s4 = int(score4.split('-')[0])
                p2s4 = int(score4.split('-')[1])
                if p1s4 > p2s4:
                    win1 += 1
                else:
                    win2 += 1
            else:
                p1s4=None
                p2s4=None

            if score5 != None:
                p1s5 = int(score5.split('-')[0])
                p2s5 = int(score5.split('-')[1])
                if p1s5 > p2s5:
                    win1 += 1
                else:
                    win2 += 1
            else:
                p1s5=None
                p2s5=None

            if win1 > win2:
                winner = data['player1']
            else:
                winner = data['player2']

            winrate = '{}-{}'.format(max(win1,win2),min(win1,win2))

            m = Match(player1=data['player1'], player2=data['player2'], score1=score1, score2=score2, score3=score3, score4=score4,
            score5=score5, date=data['date'], venue=data['venue'],
            p1s1=p1s1, p1s2=p1s2, p1s3=p1s3, p1s4=p1s4, p1s5=p1s5,
            p2s1=p2s1, p2s2=p2s2, p2s3=p2s3, p2s4=p2s4, p2s5=p2s5,
            winner=winner, winrate=winrate)

            m.save()

            p1 = data['player1']
            p2 = data['player2']
            p1.played +=1
            p2.played +=1

            if winner == p1:
                p1.won += 1
                p2.lost +=1
                p1.form = '<i class="fa-solid fa-circle-check green"></i> ' + p1.form
                p2.form = '<i class="fa-solid fa-circle-xmark red" style="color:red"> ' + p2.form
            if winner == p2:
                p2.won += 1
                p1.lost += 1
                p1.form = '<i class="fa-solid fa-circle-xmark red" style="color:red"> ' + p1.form
                p2.form = '<i class="fa-solid fa-circle-check green"></i> ' + p2.form
            p1.point = p1.won * 3
            p2.point = p2.won * 3

            p1.save()
            p2.save()

            return redirect(reverse('tt:tt_index'))
        else:
            context = {'form': adform}
            return render(request, 'tt/admin.html', context)