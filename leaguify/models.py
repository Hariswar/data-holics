from django.db import models

# Create your models here.

'''class Sport(models.Model):
    sportName = models.TextField()
    id = models.IntegerField(name='sportID', primary_key=True)
    individualSport = models.BooleanField(name='individualSport')

class Player(models.Model):
    playerID = models.IntegerField(primary_key=True)
    emailAddress = models.TextField(max_length=64, null=False)
    firstName = models.TextField(max_length=32, null=False)
    middleName = models.TextField(max_length=32)
    lastName = models.TextField(max_length=32, null=False)
    teamID = models.IntegerField()

    # def __init__(self, emailAddress: str, firstName: str, middleName: str|None, lastName: str, teamID: int|None):
        
    #     if Player.objects.count() > 0:
    #         latest = Player.objects.latest()
    #         self.playerID = latest.playerID + 1
    #     else:
    #         self.playerID = 0
    #     self.emailAddress = emailAddress
    #     self.firstName = firstName
    #     self.middleName = middleName
    #     self.lastName = lastName
    #     self.teamID = teamID
'''
from django.db import models
class Sport(models.Model):
    sportName = models.CharField(max_length=32)
    individualSport = models.BooleanField()
class Custom_User(models.Model):
    emailAddress = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=64)
    firstName = models.CharField(max_length=32)
    middleName = models.CharField(max_length=32, null=True)
    lastName = models.CharField(max_length=32)
    last_login = models.DateTimeField(null=True)
    # teamID = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
class League(models.Model):
    dateCreated = models.DateField
    leagueName = models.CharField(max_length=32)
    sportID = models.ForeignKey(Sport, on_delete=models.SET_NULL, null=True)
class Team(models.Model):
    teamName = models.CharField(max_length=32)
    leagueID = models.ForeignKey(League, on_delete=models.CASCADE, null=False)
class Player(models.Model):
    userID = models.ForeignKey(Custom_User, on_delete=models.SET_NULL, null=True)
    teamID = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
class Game(models.Model):
    winnerID = models.ForeignKey(Team, on_delete=models.CASCADE)
    # leagueID = models.ForeignKey(League, on_delete=models.SET_NULL, null=True)
    # sportID = models.ForeignKey(Sport, on_delete=models.CASCADE)
    Description = models.TextField(null=True)
class Sport_Stats(models.Model):
    teamID = models.ForeignKey(Team, on_delete=models.SET_NULL,null=True)
    score = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    leagueID = models.ForeignKey(League, on_delete=models.SET_NULL, null=True)
    sportID = models.ForeignKey(Sport, on_delete=models.CASCADE)
    eLo = models.FloatField(null=True)
    gamesPlayed = models.IntegerField(default=0)
    winPercent = models.FloatField(default=0)
class Social_Media(models.Model):
    playerID = models.ForeignKey(Player, on_delete=models.CASCADE)
    userName = models.CharField(max_length=32)
    type = models.CharField(max_length=32)
class Team_Social_Media(models.Model):
    teamID = models.ForeignKey(Team, on_delete=models.CASCADE)
    userName = models.CharField(max_length=32)
    type = models.CharField(max_length=32)
class Plays(models.Model):
    # leagueID = models.ForeignKey(League, on_delete=models.SET_NULL, null=True)
    teamID = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    gameID = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True)




