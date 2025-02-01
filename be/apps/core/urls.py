from django.urls import path
from apps.core.views.user import UserView

urlpatterns = [
    path("", UserView.as_view(), name="users"),
    path("<int:user_id>/", UserView.as_view(), name="user"),#no entiendo bien la funcion del nombre="user"
    path("<int:user_id>/", FriendsView.as_view(), name="friend"),
    path("<int:user_id>/", StatsView.as_view(), name="stats"),
    path("<str:tournament_name>/<int:tournament_id>/", TournamentsView.as_view(), name="tournament"),
]
