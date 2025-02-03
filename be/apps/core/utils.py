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


def serialize_tournament(tournaments):
    return {
        "id": tournaments.id,
        "tournament_name": tournaments.tournament_name,
        "start_date": tournaments.start_date,
        "end_date": tournaments.end_date,
        "players": [serialize_user(player) for player in tournaments.players.all()],
    }


def serialize_history(user):
    return {
        "id": user.id,
        "user_id": user.user_id,
        "result_user": user.result_user,
        "opponent": user.opponent,
        "result_opponent": user.result_opponent,
        "type_match": user.type_match,
        "tournament_id": user.tournament_id,
        "position_match": user.position_match,
        "date": user.date,
        "position_tournament": user.position_tournament,
    }
