from django import forms

from match.models import TeamScore



class TeamScoreForm(forms.ModelForm):
    team = forms.ModelChoiceField(queryset=None)
    
    class Meta:
        model = TeamScore 
        fields = ["team", "time", "player"]