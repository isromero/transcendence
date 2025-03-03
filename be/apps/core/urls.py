from django.urls import path
from apps.core.views.user import UserView
from apps.core.views.friends import FriendsView
from apps.core.views.stats import StatsView
from apps.core.views.history import HistoryView
from apps.core.views.tournaments import TournamentsView
from apps.core.views.login import LoginView
from apps.core.views.register import RegisterView
from apps.core.views.game import GameView
from apps.core.views.auth import OAuthLogin, LogoutView, OAuthCallback
# from apps.core.views.auth import OAuthLogin, auth_login, auth_callback, auth_logout

from django.urls import re_path
from . import consumers

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
    path("history", HistoryView.as_view()),
    path("history/match/<uuid:match_id>", HistoryView.as_view()),
    # Auth routes
    path("login", LoginView.as_view()),
    path("register", RegisterView.as_view()),
    path("game", GameView.as_view(), name="game"),
    path("auth/login", OAuthLogin.as_view(), name="auth_login"),
    # path("auth/callback/", auth_callback, name="auth_callback"),
    path("auth/logout/", LogoutView.as_view(), name="auth_logout"),
]
