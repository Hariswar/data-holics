from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from django.views.generic.detail import DetailView
from django.db.models import Q, Avg, Sum, Count
from django.http import HttpResponseRedirect
from .models import *
from .forms import *

import json

# DICTIONARY ADDITION (lol)
def add_dicts(lhs: dict, rhs: dict):
    new_dict = {}
    rem = rhs.keys()
    for k, v in lhs:
        new_dict[k] = v
        if k in rhs:
            new_dict[k] += rhs[k]
    for k in rem:
        new_dict[k] = rhs[rem]

# Create your views here.

# HELPER FUNCTIONS
def is_in_league(user, league):
  user = Custom_User.objects.get(emailAddress=user.username)
  players = Player.objects.filter(userID=user.id)
  teams = Team.objects.filter(leagueID_id=league.id)
  for player in players:
    for team in teams:
      if player.teamID == team:
        return True
  return False

def is_on_team(user, team):
  user = Custom_User.objects.get(emailAddress=user.username)
  players = Player.objects.filter(userID=user.id)
  for player in players:
    if player.teamID == team:
      return True
  return False

# DETAIL VIEWS

class PlayerDetailView(DetailView):
    model = Player

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sm = Social_Media.objects.filter(playerID_id=context['object'].id)
        context['social_media'] = sm
        stats = Player_Sport_Stats.objects.get(playerID_id=context['object'].id)
        context['stats'] = stats
        additional_stats = json.loads(stats.additionalStats)
        context['additional_stats'] = additional_stats
        print(context)
        return context

# DETAIL VIEWS

class LeagueDetailView(DetailView):
    model = League

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teams = Team.objects.filter(leagueID_id=context['object'].id)
        plays = Plays.objects.filter(teamID__in=teams)
        games = Game.objects.filter(id__in=plays.values('gameID'))
        games = games.values()
        for game in games:
            game['teams'] = []
            p = Plays.objects.filter(gameID_id=game['id'])
            for i in p:
                game['teams'].append(i.teamID)
        for team in teams:
            players = Player.objects.filter(teamID_id=team.id, userID__emailAddress=self.request.user.username)
            if players.count() > 0:
                context['team_creatable'] = False
                break
            else:
                context['team_creatable'] = True
        context['teams'] = [{ "team": t, "stats": Team_Sport_Stats.objects.get(teamID=t) } for t in teams]
        context['games'] = games
        return context

class TeamDetailView(DetailView):
    model = Team

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        players = Player.objects.filter(teamID_id=context['object'].id)
        social_media = Team_Social_Media.objects.filter(teamID_id=context['object'].id)
        context['players'] = players
        context['social_media'] = social_media
        stats = Team_Sport_Stats.objects.get(teamID_id=context['object'].id)
        context['stats'] = stats
        additional_stats:dict
        try:
            additional_stats = json.loads(stats.additionalStats)
        except Exception as e:
            ads = {}
            sport = context['object'].leagueID.sportID
            tracks = Tracks.objects.filter(sport=sport)
            for i in tracks:
                ads[i.statisticName] = 0
            stats.additionalStats = json.dumps(ads).encode('utf-8')
            stats.save()
            additional_stats = json.loads(stats.additionalStats)

        context['additional_stats'] = additional_stats
        if players.filter(userID__emailAddress=self.request.user.username).count() > 0:
            context['team_joinable'] = False
            context['team_editable'] = True
        else:
            context['team_editable'] = False
            players2 = Player.objects.filter(userID__emailAddress=self.request.user.username, teamID__leagueID=context['object'].leagueID)
            if players2.count() > 0:
                context['team_joinable'] = False
            else:
                context['team_joinable'] = True
        return context

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
            context = {
                "message": "Username or password is incorrect."
            }
            return render(request, 'login.html', context)
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
            user = authenticate(request, username=n_a.emailAddress, password=n_a.password)
            login(request, user)
            return redirect('user_home')
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
    return redirect('login')

def all_leagues(request):
    template = loader.get_template('public_leagues.html')
    items = []
    leagues = League.objects.all()
    for league in leagues:
        team_ct = Team.objects.filter(leagueID=league).count()
        items.append({ "league": league, "team_count": team_ct })
    context = {
        'leagues': items
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
    if request.method == 'GET':
        sports = Sport.objects.all()
        template = loader.get_template('create_league.html')
        context = {
            'sports': sports,
            'type' : 'create'
        }
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        leagueName = request.POST.get('leagueName')
        sportID = request.POST.get('sport')
        teamName = request.POST.get('yourTeamName')
        stats = {}
        for name in Tracks.objects.filter(sport_id=sportID):
            stats[name.statisticName] = 0
        empty = json.dumps(stats).encode('utf-8')
        try:
            league = None
            try:
                league = League.objects.get(leagueName=leagueName, sportID=sportID)
            except Exception as e:
                print(e)
                league = League.objects.create(leagueName=leagueName, sportID_id=sportID)
            team = Team.objects.create(teamName=teamName, leagueID_id=league.id)
            team_stats = Team_Sport_Stats.objects.create(teamID_id=team.id, additionalStats=empty)
            user = Custom_User.objects.get(emailAddress=request.user.username)
            player = Player.objects.create(teamID_id=team.id, userID_id=user.id)
            player_stats = Player_Sport_Stats.objects.create(playerID_id=player.id, additionalStats=empty)
            return redirect('user_home')
        except Exception as e:
            print(e)
            return redirect('create_league')

# CREATE NEW TEAM PAGE
@csrf_protect
def create_team(request, pk):
    if request.method == 'GET':
        template = loader.get_template('create_team.html')
        context = {}
        players = Player.objects.filter(userID=request.user.id)
        for team in players.values('teamID_id'):
            teams = Team.objects.filter(id=team['teamID_id'], leagueID_id=pk)
            if teams.count() > 0:
                context['team_creatable'] = False
                break
        else:
            context['team_creatable'] = True
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        league = League.objects.get(id=pk)
        stats = {}
        for name in Tracks.objects.filter(sport_id=league.sportID):
            stats[name.statisticName] = 0
        empty = json.dumps(stats).encode('utf-8')
        teamName = request.POST.get('teamName')
        team = Team.objects.create(teamName=teamName, leagueID_id=pk)
        print(team, request.user.id)
        user = Custom_User.objects.get(emailAddress=request.user.username)
        team_stats = Team_Sport_Stats.objects.create(teamID_id=team.id, additionalStats=empty)
        player = Player.objects.create(teamID=team, userID_id=user.id)
        player_stats = Player_Sport_Stats.objects.create(playerID_id=player.id, additionalStats=empty)
        return redirect('.')
    return redirect('.')

# USER HOME PAGE
@login_required
def user_home(request):
    user = Custom_User.objects.get(emailAddress=request.user)
    template = loader.get_template('user_home.html')
    user = Custom_User.objects.get(emailAddress=request.user.username)
    players = Player.objects.filter(userID_id=user.id)
    social_media = []
    stats = []
    additionalStats = []
    social_media = Social_Media.objects.filter(playerID__userID_id=user.id).values('userName', 'type')
    sport_stats = Player_Sport_Stats.objects.filter(playerID__userID_id=user.id)
    ss = sport_stats.values('playerID__teamID__leagueID__sportID__sportName').annotate(total_wins=Sum("wins"), total_losses=Sum("losses"), total_draws=Sum("draws"))
    for s in sport_stats:
        if s.additionalStats == None:
            s.additionalStats = json.dumps({})
    print(ss)
    teamIDs = players.values('teamID_id')
    teams = []
    for item in teamIDs: 
        if item['teamID_id'] == None:
            continue
        team = Team.objects.get(id=item['teamID_id'])
        teams.append({
            "team": team,
            "league": team.leagueID
        })

    context = {
        "teams": teams,
        "social_media": social_media,
        "stats": ss,
        "additional_stats": additionalStats,
    }
    # "general_stats": general_stats,
    # "highest_game": highest_game,
    # "sports": sports,
    # "leagues": leagues,
    return HttpResponse(template.render(context, request))
@login_required
def delete_league(request, pk):
    league = League.objects.get(id = pk)
    if request.method == 'POST':
        user = request.user
        if(is_in_league(user, league)): # Note: no 'else' statement. If bad permissions nothing happens.
          league.delete()
          return redirect('user_home')
        return render(request, 'delete.html', {'obj':league.leagueName, "message": "Can't delete this League! You must belong to a League to delete it." })
    return render(request, 'delete.html', {'obj':league.leagueName})


@login_required
def delete_team(request, pk):
    team = Team.objects.get(id = pk)
    if request.method == 'POST':
        if(is_on_team(request.user, team)):
          team.delete() 
          return redirect('user_home')
        return render(request, 'delete.html', {'obj':team.teamName, "message": "Can't delete this Team! You must belong to a Team to delete it."})
    return render(request, 'delete.html', {'obj':team.teamName})

@login_required
def create_game(request, pk):
    context = {}
    if request.method == 'POST':
        try:
            team1 = request.POST.get('team1')
            team2 = request.POST.get('team2')
            if team1 == team2: raise Exception("Both teams cannot be the same!")
            team1winner = request.POST.get('team1winner')
            team2winner = request.POST.get('team2winner')
            team1Stats = Team_Sport_Stats.objects.get(teamID_id=team1)
            team2Stats = Team_Sport_Stats.objects.get(teamID_id=team2)
            winnerID = None
            if team1winner != team2winner: 
                if team1winner:
                    winnerID = team1
                    team1Stats.wins += 1
                    team2Stats.losses += 1
                    for player_stats in Player_Sport_Stats.objects.filter(playerID__teamID=team1):
                        player_stats.wins += 1
                        player_stats.save()
                    for player_stats in Player_Sport_Stats.objects.filter(playerID__teamID=team2):
                        player_stats.losses += 1
                        player_stats.save()
                else: 
                    winnerID = team2
                    team1Stats.losses += 1
                    team2Stats.wins += 1
                    for player_stats in Player_Sport_Stats.objects.filter(playerID__teamID=team1):
                        player_stats.losses += 1
                        player_stats.save()
                    for player_stats in Player_Sport_Stats.objects.filter(playerID__teamID=team2):
                        player_stats.wins += 1
                        player_stats.save()
            else:
                if team1Stats.draws == None: team1Stats.draws = 0
                if team2Stats.draws == None: team2Stats.draws = 0
                team1Stats.draws += 1
                team2Stats.draws += 1
                for player_stats in Player_Sport_Stats.objects.filter(playerID__teamID=team1):
                    player_stats.draws += 1
                    player_stats.save()
                for player_stats in Player_Sport_Stats.objects.filter(playerID__teamID=team2):
                    player_stats.draws += 1
                    player_stats.save()
            league = League.objects.get(id=pk)
            stats = Tracks.objects.filter(sport=league.sportID)
            for stat in stats:
                team1stat = request.POST.get(f"team1{stat.statisticName}")
                team1statDict = json.loads(team1Stats.additionalStats)
                if team1stat == '': team1stat = 0
                team1statDict[stat.statisticName] += int(team1stat)
                team1Stats.additionalStats = json.dumps(team1statDict).encode('utf-8')

                team2stat = request.POST.get(f"team2{stat.statisticName}")
                team2statDict = json.loads(team2Stats.additionalStats)
                if team2stat == '': team2stat = 0
                team2statDict[stat.statisticName] += int(team2stat)
                team2Stats.additionalStats = json.dumps(team2statDict).encode('utf-8')
            team1Stats.save()
            team2Stats.save()
            game = Game.objects.create(winnerID_id=winnerID, Description=request.POST.get('description'))
            _ = Plays.objects.create(gameID=game, teamID_id=team1)
            _ = Plays.objects.create(gameID=game, teamID_id=team2)
            return redirect('.')
        except Exception as e:
            context["message"] = e
    teams = Team.objects.filter(leagueID_id=pk)
    league = League.objects.get(id=pk)
    stats = Tracks.objects.filter(sport=league.sportID)
    context["teams"] = teams
    context["stats"] = stats
    return render(request, 'create_game.html', context)


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

@csrf_protect
def add_player_social_media(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'add_player_social_media.html', context)
    elif request.method == 'POST':
        platform = request.POST.get('type')
        userName = request.POST.get('userName')
        user = Custom_User.objects.get(emailAddress=request.user.username)
        players = Player.objects.filter(userID_id=user.id)
        for player in players.iterator():
            sm = Social_Media.objects.create(type=platform, userName=userName, playerID_id=player.id)
        return HttpResponseRedirect('user_home')

@csrf_protect
def add_team_social_media(request, pk):
    if request.method == 'GET':
        context = {}
        return render(request, 'add_team_social_media.html', context)
    elif request.method == 'POST':
        platform = request.POST.get('type')
        userName = request.POST.get('userName')
        sm = Team_Social_Media.objects.create(type=platform, userName=userName, teamID_id=pk)
        return redirect('.')

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
            user = Custom_User.objects.get(emailAddress=request.user.username)
            player = Player.objects.create(teamID_id=team.id, userID_id=user.id)
            return redirect('user_home')
        except Exception as e:
            return redirect('create_league')
    return render(request, 'blank.html')

@csrf_protect 
def join_team(request, pk):
    team = Team.objects.get(pk=pk)
    user = Custom_User.objects.get(emailAddress=request.user.username)
    print(user, team)
    player = Player.objects.create(userID=user, teamID=team)
    return redirect('.')

@login_required
def create_new_sport(request):
    if request.method == 'POST':
        sportName = request.POST.get('sport')
        statistics = request.POST.get('statistics')
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
            if statistics != '':
                for stat in str(statistics).split(','):
                    tracks = Tracks.objects.create(sport=sport, statisticName=stat)
            return redirect('user_home')
        except:
            return redirect('create_sport')
    return render(request, 'create_sport.html')

@login_required
def updateLeague(request, pk):
    league = League.objects.get(id=pk)
    league_name = league.leagueName
    league_sport = league.sportID.sportName
    user = Custom_User.objects.get(emailAddress=request.user.username)
    if request.method == 'GET':
        sports = Sport.objects.all()
        template = loader.get_template('create_league.html')
        context = {
            'sports': sports,
            'selected_sport' : league_sport,
            'lname' : league_name,
            'type' : 'update',
        }
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        try:
            league.leagueName = request.POST.get('leagueName')
            league.sportID_id = request.POST.get('sport')
            league.save()
            # teamName = request.POST.get('yourTeamName')
            # teamName = ""
            # if teamName != "":
            #     try:
            #         team = Team.objects.get(teamName=teamName)
            #     except:
            #         try:
            #             stats = {}
            #             for name in Tracks.objects.filter(sport_id=league.sportID):
            #                 stats[name.statisticName] = 0
            #             empty = json.dumps(stats).encode('utf-8')
            #             team = Team.objects.create(teamName=teamName, leagueID_id = league.id)
            #             team_stats = Team_Sport_Stats.objects.create(teamID_id=team.id, additionalStats=empty)
            #             player = Player.objects.create(teamID_id=team.id, userID_id=user.id)
            #             player_stats = Player_Sport_Stats.objects.create(playerID_id=player.id, additionalStats=empty)
            #             return redirect('user_home')
            #         except Exception as e:
            #             print(e)
            #             redirect('create_league')
        except Exception as e:
            print(e)
            return redirect('create_league')
        return redirect('user_home')
    return redirect('user_home')

@login_required
def edit_team(request, pk):
    team = Team.objects.get(id=pk)
    user = Custom_User.objects.get(emailAddress=request.user.username)
    player = Player.objects.get(teamID=pk)
    league = League.objects.get(id=team.leagueID.id)
    isuser = 'false'
    if user.id == player.userID.id:
        isuser = 'true'
    if request.method == 'GET':
        leagues = League.objects.all()
        users = Custom_User.objects.all()
        template = loader.get_template('create_team.html')
        context = {
            'name' : team,
            'lcurrent' : league.leagueName,
            'leagues' : leagues,
            'users' : users,
            'cuser' : user,
            'isuser' : isuser,
            'type' : 'edit'
        }
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        n_name = request.POST.get('teamName')
        n_league = request.POST.get('leagueName')
        n_user = request.POST.get('userName')
        try:
            uleague = League.objects.get(id=n_league)
            try:
                error = Team.objects.get(teamName=team.teamName)
                if error.id != team.id and error.leagueID == uleague:
                    return redirect('update_team')
            except:
                pass
            team.teamName = n_name
            team.leagueID = uleague
            team.save()
            nuser = Custom_User.objects.get(emailAddress=n_user)
            if nuser.id != user.id:
                try:
                    uplay = Player.objects.get(userID=nuser.id, teamID__leagueID=uleague.id)
                    return redirect('update_team')
                except:
                    pass
                player.userID = nuser.id
                player.save()
            return redirect('user_home')
        except:
            pass
    return redirect('all_leagues')
def user_profile(request, pk):
    user = Custom_User.objects.get(id=pk)
    players = Player.objects.filter(userID=user)
    context = {}
    if request.method == 'GET':
        template = loader.get_template('user_profile.html')
        context['ufname'] = user.firstName
        context['umname'] = user.middleName
        context['ulname'] = user.lastName
        context['uaddress'] = user.emailAddress
        smss = []
        for player in players:
            smss += Social_Media.objects.filter(playerID=player)
        context['smss'] = smss
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        nfname = request.POST.get('fname')
        nmname = request.POST.get('mname')
        nlname = request.POST.get('lname')
        user.firstName = nfname
        user.middleName = nmname
        user.lastName = nlname
        user.save()
        return redirect('user_profile', pk)
    return redirect('user_home')

def delete_sm(request, pk):
    sm = Social_Media.objects.get(id = pk)
    if request.method == 'POST':
        sm.delete() 
        return redirect('user_home')
    return render(request, 'delete.html', {'obj':sm.userName})

def edit_sm(request, pk):
    sm = Social_Media.objects.get(id=pk)
    user = Custom_User.objects.get(id=sm.playerID.userID.id)
    if request.method == 'GET':
        context = {}
        template = loader.get_template('add_player_social_media.html')
        context['cuname'] = sm.userName
        context['ctype'] = sm.type
        context['type'] = 'edit'
        context['uid'] = user
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        nea = request.POST.get('email')
        nuname = request.POST.get('userName')
        ntype = request.POST.get('type')
        user.emailAddress = nea
        sm.userName = nuname
        sm.type = ntype
        sm.save()
        user.save()
        return redirect('user_profile', user.id)
    return redirect('user_profile', user.id)
def change_password(request, pk):
    user = Custom_User.objects.get(id=pk)
    context = {}
    if request.method == 'GET':
        template = loader.get_template('change_password.html')
        context = {'cpass' : user.password}
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        context = {}
        npass1 = request.POST.get('pass1')
        npass2 = request.POST.get('pass2')
        try: 
            if npass1 != npass2: raise Exception("Your Passwords Are Not The Same")
            user.password = npass1
            user.save()
            return redirect('user_home')
        except Exception as e:
            context["message"] = e
    return render(request, 'change_password.html', context)