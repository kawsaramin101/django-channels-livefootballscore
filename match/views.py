from django.shortcuts import render

from .models import Match


def index(request):
    matches = Match.objects.all()
    context = {
        "matches": matches,
    }
    return render(request, "match/index.html", context)
    

def match_details(request, secondary_id):
    match = Match.objects.prefetch_related("teams", "scores").get(secondary_id=secondary_id)
    team_one = match.teams.first()
    team_two = match.teams.all()[1]
    
    context = {
        "match": match,
        "team_one": team_one,
        "team_two": team_two,
    }
    return render(request, "match/match-details.html", context)
    
    