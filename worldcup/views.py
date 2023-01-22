from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Team, KnockOutTeamSelection, Comment, LeaderBoard, Score, Match
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (CommentForm, ScoreForm, KnockOutForm, NewUserForm,#RoundOf16Form, QuarterForm, SemiForm, FinalForm,
                    AdminUpdateForm, AdminQuarterForm, AdminSemiForm, AdminFinalForm, AdminChampionForm)
from django.urls import reverse
from django.contrib.auth import get_user_model, login
from .leader import update_leaderboard
from django.conf import settings
from django.contrib import messages

# Create your views here.
class HomeView(View):
    def get(self, request):
        host = request.get_host()
        islocal = host.find('localhost') >= 0 or host.find('127.0.0.1') >= 0
        context = {'installed': settings.APP_NAME, 'islocal':islocal, 'user_name': request.user}
        return render(request, 'worldcup/home_main.html', context)

def register_user(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration Successful.")
            return redirect(reverse("worldcup:worldcup_index"))
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, 'worldcup/register.html',context={"register_form":form})

class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        team_A = Team.objects.filter(group="A").order_by("-points", "-gd", "name")
        team_B = Team.objects.filter(group="B").order_by("-points", "-gd", "name")
        team_C = Team.objects.filter(group="C").order_by("-points", "-gd", "name")
        team_D = Team.objects.filter(group="D").order_by("-points", "-gd", "name")
        team_E = Team.objects.filter(group="E").order_by("-points", "-gd", "name")
        team_F = Team.objects.filter(group="F").order_by("-points", "-gd", "name")
        team_G = Team.objects.filter(group="G").order_by("-points", "-gd", "name")
        team_H = Team.objects.filter(group="H").order_by("-points", "-gd", "name")

        commentform = CommentForm()
        comment = Comment.objects.all().order_by('-created_at')
        players = LeaderBoard.objects.all().order_by('-points')

        context = {'team_A':team_A, 'team_B':team_B, 'team_C':team_C,
                    'team_D':team_D, 'team_E':team_E, 'team_F':team_F,
                    'team_G':team_G, 'team_H':team_H,
                    'commentform':commentform,
                    'comment':comment,
                    'players':players,
                    'isauth':request.user.is_authenticated}
        return render(request, 'worldcup/main.html',context)

    def post(self, request):
        comment = Comment(text=request.POST['comment'], owner=request.user)
        comment.save()
        return redirect(reverse('worldcup:worldcup_index'))

class PredictionView(LoginRequiredMixin, View):
    team_A = Team.objects.filter(group="A").order_by("-points", "-gd", "name")
    team_B = Team.objects.filter(group="B").order_by("-points", "-gd", "name")
    team_C = Team.objects.filter(group="C").order_by("-points", "-gd", "name")
    team_D = Team.objects.filter(group="D").order_by("-points", "-gd", "name")
    team_E = Team.objects.filter(group="E").order_by("-points", "-gd", "name")
    team_F = Team.objects.filter(group="F").order_by("-points", "-gd", "name")
    team_G = Team.objects.filter(group="G").order_by("-points", "-gd", "name")
    team_H = Team.objects.filter(group="H").order_by("-points", "-gd", "name")

    def get(self, request):

        initial = {}
        old_data = Score.objects.filter(owner=request.user)
        for each in old_data:
            initial[str(each.mymatch.id)] = str(each.myscore)

        anewform = ScoreForm(initial=initial)

        context = {'team_A':self.team_A, 'team_B':self.team_B, 'team_C':self.team_C,
                    'team_D':self.team_D, 'team_E':self.team_E, 'team_F':self.team_F,
                    'team_G':self.team_G, 'team_H':self.team_H,
                    'model':Match,
                    'newform': anewform,
                    'isauth':request.user.is_authenticated}
        return render(request, 'worldcup/pred.html',context)

    def post(self, request):
        anewform = ScoreForm(request.POST)
        owner = request.user
        if anewform.is_valid():
            for key, value in anewform.cleaned_data.items():
                mymatch = get_object_or_404(Match, pk=int(key))
                try:
                    newScore = get_object_or_404(Score, mymatch=mymatch, owner=owner)
                except:
                    newScore = Score(mymatch=mymatch, owner=owner)
                newScore.myscore = value
                newScore.save()
            return redirect(reverse('worldcup:worldcup_index'))
        else:
            context = {'team_A':self.team_A, 'team_B':self.team_B, 'team_C':self.team_C,
                    'team_D':self.team_D, 'team_E':self.team_E, 'team_F':self.team_F,
                    'team_G':self.team_G, 'team_H':self.team_H,
                    'newform':anewform,
                    'model':Match,
                    'isauth':request.user.is_authenticated}
            return render(request, 'worldcup/pred.html', context)

class KnockOutPredictionView(LoginRequiredMixin, View):
    team_A = Team.objects.filter(group="A").order_by("-points", "-gd", "name")
    team_B = Team.objects.filter(group="B").order_by("-points", "-gd", "name")
    team_C = Team.objects.filter(group="C").order_by("-points", "-gd", "name")
    team_D = Team.objects.filter(group="D").order_by("-points", "-gd", "name")
    team_E = Team.objects.filter(group="E").order_by("-points", "-gd", "name")
    team_F = Team.objects.filter(group="F").order_by("-points", "-gd", "name")
    team_G = Team.objects.filter(group="G").order_by("-points", "-gd", "name")
    team_H = Team.objects.filter(group="H").order_by("-points", "-gd", "name")

    def get(self, request):
        owner = request.user
        try:
            old_data = get_object_or_404(KnockOutTeamSelection, owner=owner)
            form = KnockOutForm(instance=old_data)
        except:
            form = KnockOutForm()
        context = {'team_A':self.team_A, 'team_B':self.team_B, 'team_C':self.team_C,
                    'team_D':self.team_D, 'team_E':self.team_E, 'team_F':self.team_F,
                    'team_G':self.team_G, 'team_H':self.team_H,'form':form}
        return render(request, 'worldcup/knockout.html',context)

    def post(self, request):
        form = KnockOutForm(request.POST or None)
        if form.is_valid():
            if KnockOutTeamSelection.objects.filter(owner=request.user).exists():
                obj = get_object_or_404(KnockOutTeamSelection, owner=request.user)
                form = KnockOutForm(request.POST, instance = obj)
                obj = form.save(commit=False)
                obj.save()
            else:
                form = KnockOutForm(request.POST)
                obj = form.save(commit=False)
                obj.owner = request.user
                obj.save()
            return redirect(reverse('worldcup:prediction'))
        context = {'team_A':self.team_A, 'team_B':self.team_B, 'team_C':self.team_C,
                    'team_D':self.team_D, 'team_E':self.team_E, 'team_F':self.team_F,
                    'team_G':self.team_G, 'team_H':self.team_H,'form':form}
        return render(request, 'worldcup/knockout.html',context)


class SummaryView(LoginRequiredMixin, View):
    team_A = Team.objects.filter(group="A").order_by("-points", "-gd", "name")
    team_B = Team.objects.filter(group="B").order_by("-points", "-gd", "name")
    team_C = Team.objects.filter(group="C").order_by("-points", "-gd", "name")
    team_D = Team.objects.filter(group="D").order_by("-points", "-gd", "name")
    team_E = Team.objects.filter(group="E").order_by("-points", "-gd", "name")
    team_F = Team.objects.filter(group="F").order_by("-points", "-gd", "name")
    team_G = Team.objects.filter(group="G").order_by("-points", "-gd", "name")
    team_H = Team.objects.filter(group="H").order_by("-points", "-gd", "name")

    def get(self, request):
        try:
            q1 = KnockOutTeamSelection.objects.get(owner=request.user).qf1
            q2 = KnockOutTeamSelection.objects.get(owner=request.user).qf2
            q3 = KnockOutTeamSelection.objects.get(owner=request.user).qf3
            q4 = KnockOutTeamSelection.objects.get(owner=request.user).qf4
            q5 = KnockOutTeamSelection.objects.get(owner=request.user).qf5
            q6 = KnockOutTeamSelection.objects.get(owner=request.user).qf6
            q7 = KnockOutTeamSelection.objects.get(owner=request.user).qf7
            q8 = KnockOutTeamSelection.objects.get(owner=request.user).qf8
            s1 = KnockOutTeamSelection.objects.get(owner=request.user).sf1
            s2 = KnockOutTeamSelection.objects.get(owner=request.user).sf2
            s3 = KnockOutTeamSelection.objects.get(owner=request.user).sf3
            s4 = KnockOutTeamSelection.objects.get(owner=request.user).sf4
            f1 = KnockOutTeamSelection.objects.get(owner=request.user).f1
            f2 = KnockOutTeamSelection.objects.get(owner=request.user).f2
            cha = KnockOutTeamSelection.objects.get(owner=request.user).champion
            q = [q1, q2, q3, q4, q5, q6, q7, q8]
            s = [s1, s2, s3, s4]
            f = [f1, f2]
            scores = Score.objects.filter(owner=request.user)
            context = {'team_A':self.team_A, 'team_B':self.team_B, 'team_C':self.team_C,
                    'team_D':self.team_D, 'team_E':self.team_E, 'team_F':self.team_F,
                    'team_G':self.team_G, 'team_H':self.team_H,
                    'preds':True, 'q':q, 's':s, 'f':f, 'cha':cha,'scores':scores}
        except:
            context = {'team_A':self.team_A, 'team_B':self.team_B, 'team_C':self.team_C,
                    'team_D':self.team_D, 'team_E':self.team_E, 'team_F':self.team_F,
                    'team_G':self.team_G, 'team_H':self.team_H,
                    'preds':False}

        return render(request, 'worldcup/summary.html', context)


class MatchDetailView(LoginRequiredMixin, View):
    team_A = Team.objects.filter(group="A").order_by("-points", "-gd", "name")
    team_B = Team.objects.filter(group="B").order_by("-points", "-gd", "name")
    team_C = Team.objects.filter(group="C").order_by("-points", "-gd", "name")
    team_D = Team.objects.filter(group="D").order_by("-points", "-gd", "name")
    team_E = Team.objects.filter(group="E").order_by("-points", "-gd", "name")
    team_F = Team.objects.filter(group="F").order_by("-points", "-gd", "name")
    team_G = Team.objects.filter(group="G").order_by("-points", "-gd", "name")
    team_H = Team.objects.filter(group="H").order_by("-points", "-gd", "name")

    def get(self, request, pk):
        m = get_object_or_404(Match, pk=int(pk))
        context = {'team_A':self.team_A, 'team_B':self.team_B, 'team_C':self.team_C,
                    'team_D':self.team_D, 'team_E':self.team_E, 'team_F':self.team_F,
                    'team_G':self.team_G, 'team_H':self.team_H,'match':m}

        return render(request, 'worldcup/detail.html', context)


class AdminUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_superuser:
            initial = {}
            match_obj = Match.objects.all()
            users = get_user_model().objects.all()
            for each in match_obj:
                initial[str(each.id)] = str(each.actual_score)

            anewform = AdminUpdateForm(initial=initial)
            context = {'newform':anewform, 'is_superuser':request.user.is_superuser}
            return render(request, 'worldcup/adminupdate.html', context)
        else:
            context = {'is_superuser':False}
            return render(request, 'worldcup/adminupdate.html', context)


    def post(self, request):
        anewform = AdminUpdateForm(request.POST)
        if anewform.is_valid():
            for key, value in anewform.cleaned_data.items():
                m = get_object_or_404(Match, pk=int(key))
                m.actual_score = value
                m.save()

                # Calculating & updating 'mypoints' to Score model.
                qs = Score.objects.filter(mymatch=m)
                for each in qs:
                    #print(each.mymatch, each.myscore, value, self.calculate(value,each.myscore))
                    each.mypoints = self.calculate(value,each.myscore)
                    each.save()

            update_leaderboard()
            return redirect(reverse('worldcup:worldcup_index'))
        else:
            context = {'newform': anewform}
            return render(request, 'worldcup/adminupdate.html', context)

    def calculate(self, act_score, user_score):

        exact_score_point = 7
        win_loose_draw_point = 4

        if act_score=='' or user_score=='': return 0

        teamA_act = int(act_score.split('-')[0])
        teamB_act = int(act_score.split('-')[1])
        teamA_user = int(user_score.split('-')[0])
        teamB_user = int(user_score.split('-')[1])

        if (teamA_act == teamA_user) and (teamB_act == teamB_user):
            point = exact_score_point
        elif (teamA_act < teamB_act) and (teamA_user < teamB_user):
            point = win_loose_draw_point
        elif (teamA_act > teamB_act) and (teamA_user > teamB_user):
            point = win_loose_draw_point
        elif (teamA_act == teamB_act) and (teamA_user == teamB_user):
            point = win_loose_draw_point
        else:
            point = 0

        return point


class QuarterFinalUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_superuser:
            anewform = AdminQuarterForm()
            context = {'newform':anewform, 'is_superuser':request.user.is_superuser}
            return render(request, 'worldcup/adminquarterupdate.html', context)
        else:
            context = {'is_superuser':False}
            return render(request, 'worldcup/adminquarterupdate.html', context)


    def post(self, request):
        anewform = AdminQuarterForm(request.POST)
        if anewform.is_valid():
            qflist = list(anewform.cleaned_data.values())
            self.updateUsers(qflist)
            update_leaderboard()
            return redirect(reverse('worldcup:worldcup_index'))
        else:
            context = {'newform': anewform}
            return render(request, 'worldcup/adminquarterupdate.html', context)


    def updateUsers(self, actual_list):
        users = get_user_model().objects.filter(is_superuser=False)
        for usr in users:
            try:
                point = 0
                kop = KnockOutTeamSelection.objects.get(owner=usr)
                userqflist = [kop.qf1, kop.qf2, kop.qf3, kop.qf4,kop.qf5, kop.qf6, kop.qf7, kop.qf8]
                #print(usr)
                #print(actual_list)
                #print(userqflist)
                for tm in actual_list:
                    if tm in userqflist: point+= 7
                kop.qfpoints = point
                kop.save()
                #print(point)

            except:
                pass


class SemiFinalUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_superuser:
            anewform = AdminSemiForm()
            context = {'newform':anewform, 'is_superuser':request.user.is_superuser}
            return render(request, 'worldcup/adminsemiupdate.html', context)
        else:
            context = {'is_superuser':False}
            return render(request, 'worldcup/adminsemiupdate.html', context)


    def post(self, request):
        anewform = AdminSemiForm(request.POST)
        if anewform.is_valid():
            sflist = list(anewform.cleaned_data.values())
            self.updateUsers(sflist)
            update_leaderboard()
            return redirect(reverse('worldcup:worldcup_index'))
        else:
            context = {'newform': anewform}
            return render(request, 'worldcup/adminsemiupdate.html', context)


    def updateUsers(self, actual_list):
        users = get_user_model().objects.filter(is_superuser=False)
        for usr in users:
            try:
                point = 0
                kop = KnockOutTeamSelection.objects.get(owner=usr)
                usersflist = [kop.sf1, kop.sf2, kop.sf3, kop.sf4]
                #print(usr)
                #print(actual_list)
                #print(userqflist)
                for tm in actual_list:
                    if tm in usersflist: point+= 10
                kop.sfpoints = point
                kop.save()
                #print(point)

            except:
                pass


class FinalUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_superuser:
            anewform = AdminFinalForm()
            context = {'newform':anewform, 'is_superuser':request.user.is_superuser}
            return render(request, 'worldcup/adminfinalupdate.html', context)
        else:
            context = {'is_superuser':False}
            return render(request, 'worldcup/adminfinalupdate.html', context)


    def post(self, request):
        anewform = AdminFinalForm(request.POST)
        if anewform.is_valid():
            flist = list(anewform.cleaned_data.values())
            self.updateUsers(flist)
            update_leaderboard()
            return redirect(reverse('worldcup:worldcup_index'))
        else:
            context = {'newform': anewform}
            return render(request, 'worldcup/adminfinalupdate.html', context)


    def updateUsers(self, actual_list):
        users = get_user_model().objects.filter(is_superuser=False)
        for usr in users:
            try:
                point = 0
                kop = KnockOutTeamSelection.objects.get(owner=usr)
                userflist = [kop.f1, kop.f2]
                for tm in actual_list:
                    if tm in userflist: point+= 15
                kop.fpoints = point
                kop.save()

            except:
                pass



class ChampUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_superuser:
            anewform = AdminChampionForm()
            context = {'newform':anewform, 'is_superuser':request.user.is_superuser}
            return render(request, 'worldcup/adminchampupdate.html', context)
        else:
            context = {'is_superuser':False}
            return render(request, 'worldcup/adminchampupdate.html', context)


    def post(self, request):
        anewform = AdminChampionForm(request.POST)
        if anewform.is_valid():
            clist = list(anewform.cleaned_data.values())
            self.updateUsers(clist)
            update_leaderboard()

            return redirect(reverse('worldcup:worldcup_index'))
        else:
            context = {'newform': anewform}
            return render(request, 'worldcup/adminchampupdate.html', context)


    def updateUsers(self, actual_list):
        users = get_user_model().objects.filter(is_superuser=False)
        for usr in users:
            try:
                point = 0
                kop = KnockOutTeamSelection.objects.get(owner=usr)
                userclist = [kop.champion]
                for tm in actual_list:
                    if tm in userclist: point+= 20
                kop.champpoints = point
                kop.save()

            except:
                pass


def rules(request):
    return render(request, 'worldcup/rules.html')




