from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect

from .models import *

# Create your views here.

# --- HTML PAGE VIEWS ---

# TEST PAGE
def index(request):
    return HttpResponse("This is a test i guess lol")

# PLEASE
def please_fucing_helpme(request):
    sports = Sport.objects.all().values()
    template = loader.get_template('test.html')
    context = {
        'sports': sports
    }
    return HttpResponse(template.render(context, request))

# CREATE NEW ACCOUNT PAGE
@csrf_protect
def create_acct(request):
    template = loader.get_template('create_acct.html')
    context = {}
    return HttpResponse(template.render(context, request))

# CREATE NEW LEAGUE PAGE
@csrf_protect
def create_league(request):
    template = loader.get_template('create_league.html')
    context = {}
    return HttpResponse(template.render(context, request))

# CREATE NEW TEAM PAGE
@csrf_protect
def create_team(request):
    template = loader.get_template('create_team.html')
    context = {}
    return HttpResponse(template.render(context, request))

# USER HOME PAGE
def user_home(request, user_id=0):
    template = loader.get_template('user_home.html')
    players = Player.objects.filter(id=user_id)
    teamIDs = players.values_list('id', 'teamID_id')
    teams = []
    for id in teamIDs: 
        teams.append(Team.objects.get(pk=id))
    context = {
        "teams": teams
    }
    return HttpResponse(template.render(context, request))


# --- DATABASE FUNCTIONS + REDIRECTS ---

# RESPONSE WHEN CREATING NEW ACCOUNT
# USE THIS TYPE OF FUNCTION WHEN ADDING TO THE DATABASE
@csrf_protect
def create_new_account(request):
    if request.method == 'POST':
        email = request.POST.get('emailAddress')
        firstName = request.POST.get('firstName')
        middleName = request.POST.get('middleName')
        lastName = request.POST.get('lastName')
        newp = Player()
        if Player.objects.count() > 0: newp.playerID = Player.objects.latest("playerID").playerID + 1
        else: newp.playerID = 0
        newp.emailAddress = email
        newp.firstName = firstName
        newp.middleName = (None if middleName=='' else middleName)
        newp.lastName = lastName
        newp.teamID = None
        newp.save()
        return redirect('create_acct')

    return render(request, 'blank.html')

# CREATE NEW TEAM RESPONSE
@csrf_protect
def create_new_team(request):
    if request.method == 'POST':
        return redirect('create_team')
    return render(request, 'blank.html')

# CREATE NEW TEAM RESPONSE
@csrf_protect
def create_new_league(request):
    if request.method == 'POST':
        return redirect('create_league')
    return render(request, 'blank.html')