from apps.core.models import History
from django.db import models
import secrets
import time
from apps.core.models import Tournaments
from django.http import JsonResponse

def create_response(data=None, message=None, error=None, status=200):
    response = {
        "success": error is None,
        "data": data,
        "message": message,
        "error": error
    }
    return JsonResponse(response, status=status)

def handle_form_errors(form):
    """
    Handles form validation errors and returns the first error message for each field
    """
    errors = {}
    for field, error_list in form.errors.items():
        errors[field] = error_list[0]
    
    return create_response(
        error={
            "type": "validation_error",
            "fields": errors
        },
        status=400
    )

def serialize_user(user):
    return {
        "id": user.id,
        "username": user.username,
        "avatar": user.avatar,
        "status": user.status,
        "deleted_user": user.deleted_user,
    }


def serialize_friend(friend_relation):
    return {
        "id": friend_relation.friend_id.id,
        "username": friend_relation.friend_id.username,
        "avatar": friend_relation.friend_id.avatar,
        "created_at": friend_relation.created_at,
        "status": friend_relation.status,
    }


def serialize_stats(user, user_history):
    tournament_matches = user_history.exclude(type_match="match")
    tournament_wins = tournament_matches.filter(result_user__gt=models.F('result_opponent'))
    
    return {
        "id": user.id,
        "username": user.username,
        "victories": user_history.filter(result_user__gt=models.F('result_opponent')).count(),
        "defeats": user_history.filter(result_user__lt=models.F('result_opponent')).count(),
        "total_matches": user_history.count(),
        "tournaments_victories": tournament_wins.count(),
        "tournaments_defeats": tournament_matches.count() - tournament_wins.count(),
        "total_tournaments": tournament_matches.values('tournament_id').distinct().count()
    }

def serialize_tournament(tournament):
    matches = History.objects.filter(tournament_id=tournament.id)
    
    return {
        "id": tournament.id,
        "tournament_name": tournament.tournament_name,
        "status": tournament.status,
        "current_round": tournament.current_round,
        "join_code": tournament.join_code if tournament.status == 'pending' else None,
        "players": [
            {
                "id": player.id,
                "username": player.username
            }
            for player in tournament.players.all()
        ],
        "matches": {
            "quarter_finals": [
                {
                    "match_id": str(match.match_id),
                    "match_number": match.tournament_match_number,
                    "player1": {
                        "id": match.user_id.id,
                        "username": match.user_id.username,
                        "score": match.result_user
                    },
                    "player2": {
                        "id": match.opponent_id.id,
                        "username": match.opponent_id.username,
                        "score": match.result_opponent
                    }
                }
                for match in matches.filter(type_match='tournament_quarter').distinct('match_id')
            ],
            "semi_finals": [
                {
                    "match_id": str(match.match_id),
                    "match_number": match.tournament_match_number,
                    "player1": {
                        "id": match.user_id.id,
                        "username": match.user_id.username,
                        "score": match.result_user
                    },
                    "player2": {
                        "id": match.opponent_id.id,
                        "username": match.opponent_id.username,
                        "score": match.result_opponent
                    }
                }
                for match in matches.filter(type_match='tournament_semi').distinct('match_id')
            ],
            "finals": [
                {
                    "match_id": str(match.match_id),
                    "match_number": match.tournament_match_number,
                    "player1": {
                        "id": match.user_id.id,
                        "username": match.user_id.username,
                        "score": match.result_user
                    },
                    "player2": {
                        "id": match.opponent_id.id,
                        "username": match.opponent_id.username,
                        "score": match.result_opponent
                    }
                }
                for match in matches.filter(type_match='tournament_final').distinct('match_id')
            ]
        }
    }


def serialize_history(user_history):
    return {
        "match_id": str(user_history.match_id),
        "type_match": user_history.type_match,
        "is_local": user_history.local_match,
        "is_tournament": user_history.tournament_id is not None,
        "date": user_history.date,
        "players": {
            "player1": {
                "id": user_history.user_id.id,
                "username": user_history.user_id.username,
                "score": user_history.result_user
            },
            "player2": {
                "id": user_history.opponent_id.id,
                "username": user_history.opponent_id.username,
                "score": user_history.result_opponent
            }
        },
        "tournament_info": {
            "id": user_history.tournament_id.id,
            "name": user_history.tournament_id.tournament_name,
            "match_number": user_history.tournament_match_number
        } if user_history.tournament_id else None
    }

def generate_join_code():
    """ Generates a unique 6 character code """
    allowed_chars = '23456789ABCDEFGHJKLMNPQRSTUVWXYZ'
    
    max_attempts = 10  # Avoid infinite loop
    for _ in range(max_attempts):
        code = ''.join(secrets.choice(allowed_chars) for _ in range(6))
        
        if not Tournaments.objects.filter(join_code=code).exists():
            return code

    # If after 10 attempts we don't find a unique code, we add the timestamp
    timestamp = str(int(time.time()))[-2:]  # last 2 digits of the timestamp
    code = ''.join(secrets.choice(allowed_chars) for _ in range(4))
    return code + timestamp