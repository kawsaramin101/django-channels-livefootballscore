import json

from django.shortcuts import render
from django.template.loader import render_to_string 

from asgiref.sync import sync_to_async

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from match.models import TeamScore, Match
from .forms import TeamScoreForm 
from match.views import get_match_details


class LiveFeedConsumer2(WebsocketConsumer):
    
    def connect(self):
        self.accept()
        
    def disconnect(self, close_code):
        pass 
    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        self.send(text_data=json.dumps({"message": message}))


ACTIONS = ["add_score", "add_commentary"]


class LiveFeedConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.match_id = self.scope["url_route"]["kwargs"]["match_id"]
        self.match_group_id = "match_%s" % self.match_id
        self.user = self.scope["user"]
        self.match = await Match.objects.aget(secondary_id=self.match_id)
        
        await self.channel_layer.group_add(self.match_group_id, self.channel_name)
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.match_group_id, self.channel_name)
    
    async def receive(self, text_data):
        if not self.user.is_superuser:
            return await self.close()
        text_data_json = json.loads(text_data)
        action = text_data_json.get("action")
        data = text_data_json.get("data")
        
        if not action in ACTIONS:
            return await self.close()
        await self.channel_layer.group_send(
            self.match_group_id, {"type": action, "data": data}
        )
            
    async def add_score(self, event):
        data = event.get("data")
        team_score = await TeamScore.objects.acreate(match=self.match, team_id=data["team"], player=data["player"], time=data["time"])
        
        match = await sync_to_async(Match.objects.prefetch_related("scores").get)(secondary_id=self.match_id)
        team_one = await match.teams.afirst()
        team_two = await match.teams.exclude(id=team_one.id).afirst()
    
        
        print(match, team_one, team_two)
        
        context = {
            "match": match,
            "team_one": team_one,
            "team_two": team_two,
        }
        rendered_score = await sync_to_async(render_to_string)('livefeed/partials/score-partial.html', context)
        
        await self.send(text_data=json.dumps({"action": "update_score", "rendered_html": rendered_score}))

        

