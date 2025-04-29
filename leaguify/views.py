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
    return render(request, 'create_league.html')

# CREATE NEW TEAM PAGE
@csrf_protect
def create_team(request):
    return render(request, 'create_team.html')


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