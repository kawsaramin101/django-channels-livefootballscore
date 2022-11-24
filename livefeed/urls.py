from django.urls import path

from .views import add_score

app_name = "livefeed"


urlpatterns = [
    path("add-score/<str:secondary_id>/", add_score, name="add_score"),
    
]
