from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from account.models import *
from .forms import SignUpForm, LoginForm, TeamForm
from django.contrib.auth import authenticate, login, logout

def home(request):
    username = request.user.username
    acc = Account.objects.get(username=username)
    if acc.team == None:
        context = {"team": "None"}
    else:
        context = {"team": acc.team.name}
    return render(request, "home.html", context=context)


def signup(request):
    if request.method == "GET":
        return render(request, 'signup.html' , {'form': SignUpForm})
    elif request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            login(request, authenticate(
                request, username=form.cleaned_data["username"], password=form.cleaned_data["password1"]
            ))
            return redirect("/account/team/") 
        else:
            return render(request, 'signup.html' , {'form': SignUpForm})
 
 
def login_account(request): 
    if request.method == "GET":
        return render(request, 'login.html' , {'form': LoginForm})
    elif request.method == "POST":        
        form = LoginForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = authenticate(
                request, username=form.cleaned_data["username"], password=form.cleaned_data["password"]
            )
            if user is not None:
                login(request, user)
                return redirect("/home/")
        return redirect("/account/login/")

 
def logout_account(request): 
    logout(request)
    return redirect("/account/team/") 
 
 
@login_required 
def joinoradd_team(request): 
    username = request.user.username
    acc = Account.objects.get(username=username)
    if request.method == "GET":
        if acc.team is not None:
            return redirect("/home/")
        else:
            return render(request, 'team.html' , {'form': TeamForm})
    elif request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            if Team.objects.filter(name=form.cleaned_data["name"]).count():
                acc.team = Team.objects.get(name=form.cleaned_data["name"])
                acc.save()
            else:
                team_name = form.cleaned_data["name"]
                Team.objects.create(
                    name=team_name, jitsi_url_path=f"http://meet.jit.si/{team_name}"
                )
                acc.team = Team.objects.get(name=form.cleaned_data["name"])
                acc.save()
            return redirect("/home/")
        else:
            return redirect("/home/")

def exit_team(request):
    username = request.user.username
    acc = Account.objects.get(username=username)
    acc.team = None
    acc.save()
    return redirect("/home/")