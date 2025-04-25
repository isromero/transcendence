from apps.core.models import History
from django.db import models
import secrets
import time
from apps.core.models import Tournaments
from django.http import JsonResponse
from django.core.exceptions import ValidationError
import re


def create_response(data=None, message=None, error=None, status=200):
    response = {
        "success": error is None,
        "data": data,
        "message": message,
        "error": error,
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
        error={"type": "validation_error", "fields": errors}, status=400
    )


def validate_username(username):
    """Validates username according to our rules"""
    if not username:
        raise ValidationError("Username is required")

    if not re.match("^[a-zA-Z0-9_-]+$", username):
        raise ValidationError(
            "Username can only contain letters, numbers, underscores and hyphens"
        )

    if len(username) < 3:
        raise ValidationError("Username must be at least 3 characters long")

    if len(username) > 20:
        raise ValidationError("Username must be at most 20 characters long")

    return username.lower()


def validate_password(password):
    """Validates password according to our rules"""
    if not password:
        raise ValidationError("Password is required")

    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long")

    if len(password) > 128:
        raise ValidationError("Password must be at most 128 characters long")

    if not re.search("[A-Z]", password):
        raise ValidationError("Password must contain at least one uppercase letter")

    if not re.search("[a-z]", password):
        raise ValidationError("Password must contain at least one lowercase letter")

    if not re.search("[0-9]", password):
        raise ValidationError("Password must contain at least one number")


def serialize_user(user):
    user_history = History.objects.filter(
        models.Q(user_id=user) | models.Q(opponent_id=user)
    )

    base_data = {
        "id": user.id,
        "username": user.username,
        "avatar": user.avatar,
        "is_online": user.is_online,
        "deleted_user": user.deleted_user,
        "display_name": user.tournament_display_name,
    }
    stats_data = serialize_stats_with_history(user, user_history)

    return {**base_data, **stats_data}


def serialize_friend(friend_relation):
    user_to_show = (
        friend_relation.user_id
        if friend_relation.status == "sent"
        else friend_relation.friend_id
    )

    user_history = History.objects.filter(
        models.Q(user_id=user_to_show) | models.Q(opponent_id=user_to_show)
    )

    base_data = {
        "id": user_to_show.id,
        "username": user_to_show.username,
        "avatar": (
            user_to_show.avatar.url
            if hasattr(user_to_show.avatar, "url")
            else user_to_show.avatar or "/default_avatar.webp"
        ),
        "is_online": user_to_show.is_online,
    }
    stats_data = serialize_stats_with_history(user_to_show, user_history)

    return {**base_data, **stats_data}


def serialize_stats(user, user_history):
    
    non_tournament_matches = user_history.filter(
        type_match__in=["local", "multiplayer"],
        result_user__gt=0,
        result_opponent__gt=0,
    ).filter(
        models.Q(result_user=5, result_opponent__lt=5)
        | models.Q(result_opponent=5, result_user__lt=5)
    )

    
    tournaments = (
        user_history.filter(
            type_match__in=[
                "tournament_quarter",
                "tournament_semi",
                "tournament_final",
            ],
            result_user__gt=0,
            result_opponent__gt=0,
        )
        .filter(
            models.Q(result_user=5, result_opponent__lt=5)
            | models.Q(result_opponent=5, result_user__lt=5)
        )
        .values("tournament_id")
        .distinct()
    )

    # Count the number of wins in tournaments (excluding 5-5)
    tournament_wins = (
        user_history.filter(
            type_match="tournament_final",
            result_user=5,
            result_opponent__lt=5,  
            tournament_id__in=tournaments.values("tournament_id"),
        )
        .values("tournament_id")
        .distinct()
        .count()
    )

    total_tournaments = tournaments.count()
    tournament_defeats = total_tournaments - tournament_wins

    
    victories = non_tournament_matches.filter(
        result_user=5, result_opponent__lt=5
    ).count()
    defeats = non_tournament_matches.filter(
        result_opponent=5, result_user__lt=5
    ).count()

    return {
        "id": user.id,
        "avatar": user.avatar,
        "username": user.username,
        "display_name": user.tournament_display_name,
        "victories": victories,
        "defeats": defeats,
        "total_matches": non_tournament_matches.count() + total_tournaments,
        "tournaments_victories": tournament_wins,
        "tournaments_defeats": tournament_defeats,
        "total_tournaments": total_tournaments,
    }


def serialize_stats_for_friends(user, user_history):
    matches = user_history.values(
        "match_id",
        "type_match",
        "date",
        "result_user",
        "result_opponent",
        "opponent_id__username",
        "opponent_id__avatar",
    )

    return [
        {
            "match_id": match["match_id"],
            "type": match["type_match"],
            "date": match["date"],
            "score": {
                "user": match["result_user"],
                "opponent": match["result_opponent"],
            },
            "opponent": {
                "username": match["opponent_id__username"],
                "avatar": match["opponent_id__avatar"] or "/default_avatar.webp",
            },
        }
        for match in matches
    ]


def serialize_tournament(tournament):
    matches = History.objects.filter(tournament_id=tournament.id)

    def get_match_data(match):
        match_records = matches.filter(match_id=match.match_id).order_by("-date")
        player1_record = match_records.filter(user_id=match.user_id).first()
        player2_record = match_records.filter(user_id=match.opponent_id).first()

        if not player1_record or not player2_record:
            return None

        return {
            "match_id": str(match.match_id),
            "tournament_match_number": match.tournament_match_number,
            "player1": {
                "id": player1_record.user_id.id,
                "username": player1_record.user_id.tournament_display_name,
                "score": player1_record.result_user,
                "avatar": player1_record.user_id.avatar,
            },
            "player2": {
                "id": player2_record.user_id.id,
                "username": player2_record.user_id.tournament_display_name,
                "score": player2_record.result_user,
                "avatar": player2_record.user_id.avatar,
            },
            "game_finished": max(player1_record.result_user, player2_record.result_user)
            >= 5,
        }

    def is_round_finished(round_matches):
        return bool(round_matches) and all(
            max(match["player1"]["score"], match["player2"]["score"]) >= 5
            for match in round_matches
        )

    quarter_matches = [
        get_match_data(match)
        for match in matches.filter(type_match="tournament_quarter").distinct(
            "match_id"
        )
    ]
    semi_matches = [
        get_match_data(match)
        for match in matches.filter(type_match="tournament_semi").distinct("match_id")
    ]
    final_matches = [
        get_match_data(match)
        for match in matches.filter(type_match="tournament_final").distinct("match_id")
    ]

    # Get players in order of joining this specific tournament
    ordered_players = (
        tournament.players.through.objects.filter(tournaments=tournament)
        .order_by("id")
        .values_list("user", flat=True)
    )

    players_dict = {player.id: player for player in tournament.players.all()}

    ordered_player_objects = [players_dict[player_id] for player_id in ordered_players]

    return {
        "id": tournament.id,
        "start_date": tournament.start_date,
        "tournament_name": tournament.tournament_name,
        "status": tournament.status,
        "current_players": tournament.players.count(),
        "max_players": tournament.max_players,
        "current_round": tournament.current_round,
        "join_code": tournament.join_code,
        "players": [
            {
                "id": player.id,
                "username": player.tournament_display_name,
                "avatar": player.avatar,
            }
            for player in ordered_player_objects
        ],
        "matches": {
            "quarter_finals": quarter_matches,
            "semi_finals": semi_matches,
            "finals": final_matches,
            "round_finished": {
                "quarter_finals": is_round_finished(quarter_matches),
                "semi_finals": is_round_finished(semi_matches),
                "finals": is_round_finished(final_matches),
            },
        },
    }


def serialize_history(user_history):
    return {
        "match_id": str(user_history.match_id),
        "type_match": user_history.type_match,
        "is_tournament": user_history.tournament_id is not None,
        "date": user_history.date,
        "players": {
            "player1": {
                "id": user_history.user_id.id,
                "username": user_history.user_id.username,
                "score": user_history.result_user,
                "avatar": user_history.user_id.avatar,
            },
            "player2": {
                "id": user_history.opponent_id.id,
                "username": user_history.opponent_id.username,
                "score": user_history.result_opponent,
                "avatar": user_history.opponent_id.avatar,
            },
        },
        "tournament_info": (
            {
                "id": user_history.tournament_id.id,
                "name": user_history.tournament_id.tournament_name,
                "tournament_match_number": user_history.tournament_match_number,
            }
            if user_history.tournament_id
            else None
        ),
    }


def generate_join_code():
    """Generates a unique 6 character code"""
    allowed_chars = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"

    max_attempts = 10  # Avoid infinite loop
    for _ in range(max_attempts):
        code = "".join(secrets.choice(allowed_chars) for _ in range(6))

        if not Tournaments.objects.filter(join_code=code).exists():
            return code

    # If after 10 attempts we don't find a unique code, we add the timestamp
    timestamp = str(int(time.time()))[-2:]  # last 2 digits of the timestamp
    code = "".join(secrets.choice(allowed_chars) for _ in range(4))
    return code + timestamp


def serialize_stats_with_history(user, user_history):
    
    user_history = user_history.filter(
        models.Q(user_id=user) | models.Q(opponent_id=user)
    )

    
    unique_matches = user_history.values('match_id').distinct()
    match_ids = [match['match_id'] for match in unique_matches]

    
    unique_history = user_history.filter(match_id__in=match_ids).distinct('match_id')

    
    unique_history = unique_history.exclude(
        models.Q(result_user=0, result_opponent=0)
    ).filter(
        
        models.Q(result_user=5) | models.Q(result_opponent=5)
    )

    
    normal_matches = unique_history.filter(
        type_match__in=["local", "multiplayer"]
    )

    
    tournament_matches = unique_history.filter(
        type_match__in=["tournament_quarter", "tournament_semi", "tournament_final"]
    )

    
    normal_wins = normal_matches.filter(
        models.Q(
            
            models.Q(type_match="local", user_id=user, result_user=5) |
            
            models.Q(type_match="multiplayer") & (
                models.Q(user_id=user, result_user=5) |
                models.Q(opponent_id=user, result_opponent=5)
            )
        )
    ).count()

    normal_losses = normal_matches.filter(
        models.Q(
            
            models.Q(type_match="local", user_id=user, result_opponent=5) |
            
            models.Q(type_match="multiplayer") & (
                models.Q(user_id=user, result_opponent=5) |
                models.Q(opponent_id=user, result_user=5)
            )
        )
    ).count()

    
    tournament_wins = tournament_matches.filter(
        models.Q(user_id=user, result_user=5) |
        models.Q(opponent_id=user, result_opponent=5)
    ).count()

    tournament_losses = tournament_matches.filter(
        models.Q(user_id=user, result_opponent=5) |
        models.Q(opponent_id=user, result_user=5)
    ).count()

    
    matches = user_history.values(
        "match_id",
        "type_match",
        "date",
        "result_user",
        "result_opponent",
        "user_id",
        "user_id__username",
        "user_id__avatar",
        "opponent_id",
        "opponent_id__username",
        "opponent_id__avatar",
    ).distinct('match_id')

    match_history = []
    for match in matches:
        
        is_player1 = match["user_id"] == user.id
        
        
        if is_player1:
            player1_username = match["user_id__username"]
            player1_avatar = match["user_id__avatar"] or "/default_avatar.webp"
            player1_score = match["result_user"]
            player2_username = match["opponent_id__username"]
            player2_avatar = match["opponent_id__avatar"] or "/default_avatar.webp"
            player2_score = match["result_opponent"]
        else:
            player1_username = match["opponent_id__username"]
            player1_avatar = match["opponent_id__avatar"] or "/default_avatar.webp"
            player1_score = match["result_opponent"]
            player2_username = match["user_id__username"]
            player2_avatar = match["user_id__avatar"] or "/default_avatar.webp"
            player2_score = match["result_user"]

        match_history.append({
            "match_id": match["match_id"],
            "type": match["type_match"],
            "date": match["date"],
            "players": {
                "player1": {
                    "username": player1_username,
                    "avatar": player1_avatar,
                    "score": player1_score,
                },
                "player2": {
                    "username": player2_username,
                    "avatar": player2_avatar,
                    "score": player2_score,
                },
            }
        })

    return {
        "victories": normal_wins,
        "defeats": normal_losses,
        "tournaments_victories": tournament_wins,
        "tournaments_defeats": tournament_losses,
        "total_matches": len(match_history),
        "match_history": match_history,
    }
