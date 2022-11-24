from django.urls import path

from .views import index, match_details

app_name = "match"


urlpatterns = [
    path("", index, name="index"),
    
    path("match/<str:secondary_id>/", match_details, name="match_details")
]
