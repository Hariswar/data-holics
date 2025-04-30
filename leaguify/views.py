from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# from django.contrib.auth.models import User
from .models import *
from .forms import *

# Create your views here.

# --- HTML PAGE VIEWS ---

# TEST PAGE
def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            print(get_user(request))
            return redirect('user_home')
        else:
            return HttpResponse("USERNAME OR PASSWORD DOES NOT EXIST")
        # try:
        #     u = authenticate(request, username=email, password=password)
        #     print(u)
        #     user = User.objects.get(username=email)
        # except:
        #     return HttpResponse("USER DOES NOT EXIST")
        # if(user.password != password):
        #     user = None
        # context = {'page':page}
    return render(request, 'login.html')
def logoutUser(request):
    logout(request)
    return redirect('login')
def registerPage(request):
    if request.method == 'POST':
        try:
            n_a = User.objects.create_user(request.POST.get('email'), request.POST.get('email'), request.POST.get('password'))
            print("user")
            n_a = Custom_User.objects.create(
                emailAddress=request.POST.get('email'),
                password=request.POST.get('password'),
                firstName=request.POST.get('fname'),
                middleName=request.POST.get('mname'),
                lastName=request.POST.get('lname'),
            )
            print("custom")
            return redirect('login')
        except Exception as e:
            print(e)
            return redirect('register')
    context = {}
    return render(request, 'register.html', context)
def index(request):
    user = None
    try:
        user = Custom_User.objects.get(emailAddress=request.user)
    except:
        user = None
    if user is not None:
        return redirect('user_home')
    return render(request, 'blank.html')

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
    sports = Sport.objects.all()
    template = loader.get_template('create_league.html')
    context = {
        'sports': sports
    }
    return HttpResponse(template.render(context, request))

# CREATE NEW TEAM PAGE
@csrf_protect
def create_team(request):
    
    template = loader.get_template('create_team.html')
    context = {}
    return HttpResponse(template.render(context, request))

# USER HOME PAGE
@login_required
def user_home(request):
    user = Custom_User.objects.get(emailAddress=request.user)
    template = loader.get_template('user_home.html')
    players = Player.objects.filter(id=request.user.id)
    teamIDs = players.values('teamID_id')
    teams = []
    for item in teamIDs: 
        team = Team.objects.get(id=item['teamID_id'])
        teams.append({
            "team": team,
            "league": team.leagueID
        })
    context = {
        "teams": teams
    }
    return HttpResponse(template.render(context, request))

@login_required
def create_game(request):
    if request.method == 'POST':
        try:
            didWin = request.POST.get('win')
            team = None
            if didWin == 'yes':
                player = Player.objects.get(userID__emailAddress=request.user)
                team = player.teamID
            else:
                try:
                    winner = request.POST.get('teamWin')
                    team = Team.objects.get(teamName=winner)
                except:
                    return redirect('create_game')
            desc = request.POST.get('description')
            new_game = Game.objects.create(team,desc)
            return redirect('home')
        except:
            return redirect('create_game')
    return render(request, 'create_game.html')
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
    
    return render(request, 'create_team.html')

# CREATE NEW TEAM RESPONSE
@csrf_protect
def create_new_league(request):
    if request.method == 'POST':
        leagueName = request.POST.get('leagueName')
        sportID = request.POST.get('sport')
        teamName = request.POST.get('yourTeamName')
        try:
            league = League.objects.create(leagueName=leagueName, sportID_id=sportID)
            team = Team.objects.create(teamName=teamName, leagueID_id=league.id)
            player = Player.objects.create(teamID_id=team.id, userID_id=request.user.id)
            return redirect('user_home')
        except Exception as e:
            return redirect('create_league')
    return render(request, 'blank.html')

@login_required
def create_new_sport(request):
    if request.method == 'POST':
        sportName = request.POST.get('sport')
        i = None
        try:
            i=Sport.objects.get(sportName=sportName)
        except:
            i=None
        if i is not None:
            return redirect('create_sport')
        isIndividual = request.POST.get('individual')
        if isIndividual == "yes":
            isIndividual = True
        else:
            isIndividual = False
        try:
            sport = Sport.objects.create(sportName=sportName, individualSport=isIndividual)
            return redirect('user_home')
        except:
            return redirect('create_sport')
    return render(request, 'create_sport.html')