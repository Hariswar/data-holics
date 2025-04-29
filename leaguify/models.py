from django.db import models

# Create your models here.

class Sport(models.Model):
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


