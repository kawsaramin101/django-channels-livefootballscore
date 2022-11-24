from django.shortcuts import render

from match.models import Match
from .forms import TeamScoreForm 


def add_score(request, secondary_id):
    match = Match.objects.prefetch_related("teams").get(secondary_id=secondary_id)
    form = TeamScoreForm()
    form.fields['team'].queryset = match.teams.all()
    context = {
        "form": form,
        "match": match,
    }
    return render(request, "livefeed/add-score.html", context)
       