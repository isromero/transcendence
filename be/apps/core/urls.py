from django.urls import path
from apps.core.views.user import UserView
from apps.core.views.friends import FriendsView
from apps.core.views.stats import StatsView
from apps.core.views.history import HistoryView
from apps.core.views.tournaments import TournamentsView

urlpatterns = [
    path("users", UserView.as_view()),
    path("users/<int:user_id>", UserView.as_view()),
    path("friends", FriendsView.as_view()),
    path("friends/<int:user_id>", FriendsView.as_view()),
    path("friends/<int:user_id>/<int:friend_id>", FriendsView.as_view()),
    path("friends/<int:user_id>/<int:friend_id>/<str:action>", FriendsView.as_view()),
    path("stats/<int:user_id>", StatsView.as_view()),
    path("stats", StatsView.as_view()),
    path(
        "tournaments/<str:tournament_name>/<int:tournament_id>",
        TournamentsView.as_view(),
    ),
    path("history", HistoryView.as_view()),
]
