from django.urls import path
from apps.core.views.user import UserView
from apps.core.views.friends import FriendsView
from apps.core.views.history import HistoryView
from apps.core.views.tournaments import TournamentsView
from apps.core.views.login import LoginView
from apps.core.views.register import RegisterView
from apps.core.views.game import GameView
from apps.core.views.oauth import OAuthCallback, OAuthLogin

from apps.core.views.check_auth import CheckAuthView
from apps.core.views.profile import ProfileView
from apps.core.views.logout import LogoutView

urlpatterns = [
    # Profile route
    path("profile", ProfileView.as_view()),
    # Users routes
    path("users", UserView.as_view()),
    path("users/<int:user_id>", UserView.as_view()),
    path("users/<str:action>", UserView.as_view()),
    # Friends routes
    path("friends", FriendsView.as_view()),
    path("friends/<int:user_id>/<str:action>", FriendsView.as_view()),
    # Game routes
    path("game", GameView.as_view()),
    # Tournaments routes
    path("tournaments", TournamentsView.as_view()),
    path("tournaments/<str:join_code>", TournamentsView.as_view()),
    # History routes (only match information)
    path("history", HistoryView.as_view()),
    path("history/match/<uuid:match_id>", HistoryView.as_view()),
    # Auth routes
    path("login", LoginView.as_view()),
    path("register", RegisterView.as_view()),
    path("logout", LogoutView.as_view()),
    path("check-auth", CheckAuthView.as_view()),
    # OAuth routes
    path("oauth/login", OAuthLogin.as_view()),
    path("oauth/callback", OAuthCallback.as_view()),
    # ! Only use for testing with Postman/Other tools
    # path("auth/token-login", LoginWithToken.as_view(), name="token_login"),
]
