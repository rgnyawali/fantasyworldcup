from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth import get_user_model, login
from django.contrib import messages
#from .forms import NewUserForm
# Create your views here.

class HomeView(View):
    def get(self, request):
        context={'user':'USER'}
        return render(request, 'home/main.html',context)

def register_user(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration Successful.")
            return redirect("worldcup:worldcup_index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, 'worldcup/register.html',context={"register_form":form})
