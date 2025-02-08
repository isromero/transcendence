from django.urls import path
from apps.core.views.user import UserView
from apps.core.views.friends import FriendsView
from apps.core.views.stats import StatsView
from apps.core.views.history import HistoryView
from apps.core.views.tournaments import TournamentsView

urlpatterns = [
    path("users", UserView.as_view()),
    #GET informacion de todos usuarios #POST crear un usuario #DELETE eliminat un usuario
    path("users/<int:user_id>", UserView.as_view()),
    #GET informacion de un usuario #PUT actualizar un usuario

    path("friends", FriendsView.as_view()),
    path("friends/<int:user_id>", FriendsView.as_view()),
    path("friends/<int:user_id>/<int:friend_id>", FriendsView.as_view()),
    path("friends/<int:user_id>/<int:friend_id>/<str:action>", FriendsView.as_view()),

    path("<int:user_id>/stats", StatsView.as_view()),
    #GET acceder a estadistica de un usuario #PUT actualizar #DELETE eliminar
    #path("stats", StatsView.as_view()),#si eliminamos modelo stats, no hace falta el POST ni PUT
    #POST crea una nueva estadistica

    path("tournaments/<int:tournament_id>", TournamentsView.as_view()),
    #GET de un torneo especifico #PUT actualizacion de datos #DELETE eliminar un torneo
    path("tournaments", TournamentsView.as_view()),
    #GET de todos torneos #POST de un nuevo torneo, con todos los participantes
    
    path("history/<int:history_id>", HistoryView.as_view()),
    #PUT cambio de un historial en concreto #DELETE de un historial
    path("history/<str:action>/<int:user_id>", HistoryView.as_view()),
    #GET historial de un usuario #DELETE eliminar historial de un usuario
    path("history", HistoryView.as_view()),
    #POST crear historial de un usuario
]
