import uuid 

from django.db import models




class Team(models.Model):
    
    secondary_id = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    

class Match(models.Model):
    
    MATCH_STATUS_OPTIONS = (
        ("upcoming", "Up Coming"),
        ("live", "Live"),
        ("ended", "ended"),
        ("cancelled", "Cancelled"),
    ) 
    
    secondary_id = models.UUIDField(default=uuid.uuid4, editable=False)
    teams = models.ManyToManyField(Team, related_name="participated_matches")
    starts = models.DateTimeField()
    match_status = models.CharField(choices=MATCH_STATUS_OPTIONS, max_length=20)
    
    @property
    def first_team(self):
        return self.teams.first() 
        
    @property 
    def second_team(self):
        return self.teams.exclude(id=self.first_team.id).first()
    
    def __str__(self):
        return str(self.id)
        #return f"{self.teams.afirst()} vs {self.teams.exclude(id=self.teams.afirst().id).afirst()}"#exclude(id=team_one.id).afirst()
        #return f"{self.first_team} vs {self.second_team}"
    
    @property
    def name(self):
        return f"{self.first_team} vs {self.second_team}"
    
    
    
    
class TeamScore(models.Model):
    
    secondary_id = models.UUIDField(default=uuid.uuid4, editable=False)
    match = models.ForeignKey(Match, related_name="scores", on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name="scores", on_delete=models.CASCADE)
    time = models.PositiveSmallIntegerField()
    player = models.CharField(max_length=200)
    
    class Meta:
        ordering = ["-time"]
    