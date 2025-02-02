def serialize_user(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "avatar": user.avatar,
        "status": user.status,
    }

def serialize_friend(user):
    return {
        "id": user.id,
        "user_id": user.user_id,
        "friend_id": user.friend_id,
        "created_at": user.created_at,
        "status": user.status,
    }
    
def serialize_stats(user):
    return {
        "id": user.id,
        "user_id": user.user_id,
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
        "players": tournaments.players,
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