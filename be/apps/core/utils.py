from apps.core.models import History

def serialize_user(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "avatar": user.avatar,
        "status": user.status,
    }


def serialize_friend(friend_relation):
    return {
        "id": friend_relation.friend_id.id,
        "username": friend_relation.friend_id.username,
        "avatar": friend_relation.friend_id.avatar,
        "created_at": friend_relation.created_at,
        "status": friend_relation.status,
    }


def serialize_stats(user):
    return {
        "id": user.id,
        "user_id": user.user_id.username,
        "victories": user.victories,
        "defeats": user.defeats,
        "total_matches": user.total_matches,
        "total_tournaments": user.total_tournaments,
        "tournaments_victories": user.tournaments_victories,
    }


def serialize_tournament(tournament):
    return {
        "id": tournament.id,
        "tournament_name": tournament.tournament_name,
        "start_date": tournament.start_date,
        "end_date": tournament.end_date,
        "players": [
            {
                "user_id": player.id,
                "username": player.username,
            }
            for player in tournament.players.all()
        ],
        "matches": [
            {
                "player1": match.user_id.username,
                "punctuation_player1": match.result_user,
                "player2": match.opponent.username,
                "punctuation_player2": match.result_opponent,
            }
            for match in History.objects.filter(tournament_id=tournament.id)
        ]
    }

def serialize_tournaments(tournament):
    return {
        "id": tournament.id,
        "tournament_name": tournament.tournament_name,
        "start_date": tournament.start_date,
        "end_date": tournament.end_date,
        "players": [
            {
                "user_id": player.id,
                "username": player.username,
                "position": History.objects.filter(user_id=player, tournament_id=tournament.id)
                .order_by("position_tournament")
                .values_list("position_tournament", flat=True)
                .first()
            }
            for player in tournament.players.all()
        ],
    }


def serialize_history(user_history):
    return {
        "id": user_history.id,
        "user_id": user_history.user_id.id,
        "result_user": user_history.result_user,
        "opponent": user_history.opponent.id,
        "result_opponent": user_history.result_opponent,
        "type_match": user_history.type_match,
        "tournament_id": user_history.tournament_id.id if user_history.tournament_id else None,
        "position_match": user_history.position_match,
        "date": user_history.date,
        "position_tournament": user_history.position_tournament,
    }
