from django.urls import path
from apps.core.views.user import UserView
from apps.core.views.friends import FriendsView
from apps.core.views.stats import StatsView
from apps.core.views.history import HistoryView
from apps.core.views.tournaments import TournamentsView

urlpatterns = [
    # Users routes
    path("users", UserView.as_view()),
    path("users/<int:user_id>", UserView.as_view()),

    # Friends routes
    path("friends", FriendsView.as_view()),
    path("friends/<int:user_id>/<int:friend_id>", FriendsView.as_view()),
    path("friends/<int:user_id>/<int:friend_id>/<str:action>", FriendsView.as_view()),

    # Stats routes
    path("stats/<int:user_id>", StatsView.as_view()),
    
    # Tournaments routes
    path("tournaments", TournamentsView.as_view()),
    path("tournaments/<str:join_code>", TournamentsView.as_view()),
    
    # History routes (only match information)
    path("history/match/<uuid:match_id>", HistoryView.as_view()),
]
