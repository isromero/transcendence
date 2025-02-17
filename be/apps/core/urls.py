from django.urls import path
from apps.core.views.user import UserView
from apps.core.views.friends import FriendsView
from apps.core.views.stats import StatsView
from apps.core.views.history import HistoryView
from apps.core.views.tournaments import TournamentsView
from apps.core.views.login import LoginView
from apps.core.views.register import RegisterView
from apps.core.views.game import GameView

urlpatterns = [
    path("users", UserView.as_view()),
    path("users/<int:user_id>", UserView.as_view()),
    path("friends", FriendsView.as_view()),
    path("friends/<int:user_id>", FriendsView.as_view()),
    path("friends/<int:user_id>/<int:friend_id>", FriendsView.as_view()),
    path("friends/<int:user_id>/<int:friend_id>/<str:action>", FriendsView.as_view()),
    path("stats/<int:user_id>", StatsView.as_view()),
    path("tournaments/<int:tournament_id>", TournamentsView.as_view()),
    path("tournaments", TournamentsView.as_view()),
    path("history/<int:history_id>", HistoryView.as_view()),
    path("history/<str:action>/<int:user_id>", HistoryView.as_view()),
    path("history", HistoryView.as_view()),
    path("login", LoginView.as_view()),
    path("register", RegisterView.as_view()),
     path('game', GameView.as_view(), name='game'),
]
