import json

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

from match.models import TeamScore, Match
from .forms import TeamScoreForm 


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
        #data["match_id"] = self.match_id 
        #team_score = await TeamScore.objects.acreate(match=self.match, team_id=data["team"], player=data["player"], time=data["time"])
        form = TeamScoreForm(data)
        #form.fields['team'].queryset = match.teams.all()
        print(form)
        if form.is_valid():
            team_score = form.save(commit=false)
            team_score.match_id = self.match_id 
            print(team_score)
            await team_score.asave()
        await self.send(text_data=json.dumps({"data": team_score}))

        

