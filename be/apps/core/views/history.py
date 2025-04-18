from django.views import View
from apps.core.models import History, User
from apps.core.utils import create_response
import json
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from apps.core.views.tournaments import TournamentsView


@method_decorator(csrf_exempt, name="dispatch")
class HistoryView(View):
    def get(self, _, match_id=None):
        """Get match information by match_id"""
        try:
            matches = History.objects.filter(match_id=match_id)
            if not matches.exists():
                return create_response(error="Match not found", status=404)

            match = matches.first()
            game_finished = max(match.result_user, match.result_opponent) >= 5

            match_data = {
                "match_id": str(match.match_id),
                "is_tournament": match.tournament_id is not None,
                "type_match": match.type_match,
                "status": "finished" if game_finished else "in_progress",
                "can_play": not game_finished,
                "players": (
                    # For local matches, only two fixed players
                    [
                        {
                            "id": match.user_id.id,
                            "username": match.user_id.username,
                            "score": match.result_user,
                            "is_winner": match.result_user >= 5,
                            "is_player1": True,
                            "avatar": match.user_id.avatar,
                        },
                        {
                            "id": match.opponent_id.id,
                            "username": match.opponent_id.username,
                            "score": match.result_opponent,
                            "is_winner": match.result_opponent >= 5,
                            "is_player1": False,
                            "avatar": match.opponent_id.avatar,
                        },
                    ]
                    if match.type_match == "local"
                    else
                    # For tournaments, use the loop to get both perspectives
                    [
                        {
                            "id": history.user_id.id,
                            "username": history.user_id.username,
                            "score": history.result_user,
                            "is_winner": history.result_user >= 5,
                            "is_player1": history.user_id == match.user_id,
                            "avatar": history.user_id.avatar,
                        }
                        for history in matches
                    ]
                ),
                "tournament_info": (
                    {
                        "id": match.tournament_id.id,
                        "name": match.tournament_id.tournament_name,
                        "match_number": match.tournament_match_number,
                        "status": match.tournament_id.status,
                        "current_round": match.tournament_id.current_round,
                    }
                    if match.tournament_id
                    else None
                ),
            }
            return create_response(data=match_data)
        except Exception as e:
            return create_response(error=str(e), status=400)

    def post(self, request):
        """Create a new match (local matches) for tournaments you have to use the put of TournamentsView"""
        try:
            data = json.loads(request.body)
            if not data.get("type_match", False):
                return create_response(
                    error="Only local matches can be created", status=400
                )

            match_id = uuid.uuid4()
            user = User.objects.get(id=request.user.id)

            History.objects.create(
                match_id=match_id,
                user_id=user,
                opponent_id=user,
                type_match="local",
                result_user=0,
                result_opponent=0,
            )

            match_data = {
                "match_id": str(match_id),
                "type_match": "local",
                "status": "in_progress",
                "players": [
                    {
                        "id": request.user.id,
                        "username": request.user.username,
                        "score": 0,
                        "is_player1": True,
                    },
                    {
                        "id": request.user.id,
                        "username": request.user.username,
                        "score": 0,
                        "is_player1": False,
                    },
                ],
            }
            return create_response(
                data=match_data, message="Local match created successfully", status=201
            )
        except json.JSONDecodeError:
            return create_response(error="Invalid JSON", status=400)

    def put(self, request, match_id=None):
        """Update match score"""
        try:
            matches = History.objects.filter(match_id=match_id)
            if not matches.exists():
                return create_response(error="Match not found", status=404)

            # Verify if the match is finished
            match = matches.first()
            if max(match.result_user, match.result_opponent) >= 5:
                return create_response(
                    error="This match is already finished", status=400
                )

            data = json.loads(request.body)
            is_player1 = data.get("is_player1", True)

            # For local matches, update the corresponding score
            if match.type_match == "local":
                if is_player1:
                    match.result_user += 1
                else:
                    match.result_opponent += 1
                match.save()

                return create_response(
                    data={
                        "match_id": str(match_id),
                        "players": [
                            {
                                "id": match.user_id.id,
                                "username": match.user_id.username,
                                "score": match.result_user,
                                "is_player1": True,
                            },
                            {
                                "id": match.opponent_id.id,
                                "username": match.opponent_id.username,
                                "score": match.result_opponent,
                                "is_player1": False,
                            },
                        ],
                        "game_finished": max(match.result_user, match.result_opponent)
                        >= 5,
                    }
                )

            # Get both history records for this match
            matches = History.objects.filter(match_id=match_id)
            if not matches.exists():
                return create_response(error="Match not found", status=404)

            # Find the records for scoring user and opponent
            scoring_record = matches.get(user_id=request.user.id)
            opponent_record = matches.exclude(user_id=request.user.id).first()

            # Increment score
            if is_player1:
                scoring_record.result_user += 1
            else:
                opponent_record.result_opponent += 1

            # Check if game is finished (score of 5)
            game_finished = (
                max(scoring_record.result_user, opponent_record.result_opponent) >= 5
            )

            # Save both records
            scoring_record.save()
            opponent_record.save()

            # If it's a tournament match and game is finished, process tournament logic
            if scoring_record.tournament_id and game_finished:
                tournaments_view = TournamentsView()
                tournaments_view.process_tournament_match(scoring_record)

            return create_response(
                data={
                    "match_id": str(match_id),
                    "players": [
                        {
                            "id": scoring_record.user_id.id,
                            "username": scoring_record.user_id.username,
                            "score": scoring_record.result_user,
                            "is_player1": is_player1,
                        },
                        {
                            "id": opponent_record.user_id.id,
                            "username": opponent_record.user_id.username,
                            "score": opponent_record.result_opponent,
                            "is_player1": not is_player1,
                        },
                    ],
                    "game_finished": game_finished,
                }
            )

        except Exception as e:
            return create_response(error=str(e), status=400)
