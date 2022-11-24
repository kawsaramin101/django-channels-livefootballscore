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
    
    def __str__(self):
        return f"{self.teams.first()} vs {self.teams.all()[1]}"
    
    
class TeamScore(models.Model):
    
    secondary_id = models.UUIDField(default=uuid.uuid4, editable=False)
    match = models.ForeignKey(Match, related_name="scores", on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name="scores", on_delete=models.CASCADE)
    time = models.PositiveSmallIntegerField()
    player = models.CharField(max_length=200)
    
    class Meta:
        ordering = ["-time"]
    