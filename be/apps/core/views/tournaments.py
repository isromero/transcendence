from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from apps.core.models import Tournaments, History, User
from apps.core.utils import (
    generate_join_code,
    serialize_tournament,
    create_response,
    handle_form_errors,
)
import json
import random
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import uuid
from apps.core.forms.tournaments import TournamentsForm


@method_decorator(csrf_exempt, name="dispatch")
class TournamentsView(View):
    def get(self, _, join_code=None):
        """Get tournament information when joining a tournament"""
        try:
            if join_code:
                tournament = get_object_or_404(Tournaments, join_code=join_code)
                if tournament.status != "pending":
                    return JsonResponse(
                        {"error": "Tournament is not accepting players"}, status=400
                    )

                return JsonResponse(
                    {
                        "id": tournament.id,
                        "tournament_name": tournament.tournament_name,
                        "current_players": tournament.players.count(),
                        "max_players": tournament.max_players,
                        "status": tournament.status,
                        "players": [
                            {"id": player.id, "username": player.username}
                            for player in tournament.players.all()
                        ],
                        "join_code": tournament.join_code,
                        "start_date": tournament.start_date,
                    }
                )
        except Exception as e:
            return create_response(error=str(e), status=400)

    def post(self, request):
        """Creates a new tournament"""
        try:
            data = json.loads(request.body)
            form = TournamentsForm(data)

            if not form.is_valid():
                return handle_form_errors(form)

            tournament = form.save(commit=False)
            tournament.join_code = generate_join_code()
            tournament.status = "pending"
            tournament.save()

            # Add the creator as the first player
            tournament.players.add(request.user)
            tournament.save()

            return create_response(
                data=serialize_tournament(tournament),
                message="Tournament created successfully",
                status=201,
            )
        except Exception as e:
            return create_response(error=str(e), status=400)

    def put(self, request, tournament_id=None):
        """Handles joining the tournament and starting the tournament"""
        try:
            data = json.loads(request.body)
            action = data.get("action")

            if action == "join":
                join_code = data.get("join_code")
                tournament = get_object_or_404(Tournaments, join_code=join_code)

                if tournament.status != "pending":
                    return JsonResponse(
                        {"error": "Tournament is not accepting players"}, status=400
                    )

                if tournament.players.count() >= tournament.max_players:
                    return JsonResponse({"error": "Tournament is full"}, status=400)

                tournament.players.add(request.user)

                # If we reach the necessary number of players, change the status
                if tournament.players.count() >= 4:
                    tournament.status = "ready"

                tournament.save()
                return JsonResponse(
                    {"message": "Joined tournament successfully"}, status=200
                )

            elif action == "start":
                tournament = get_object_or_404(Tournaments, id=tournament_id)
                if tournament.status != "ready":
                    return JsonResponse(
                        {"error": "Tournament is not ready to start"}, status=400
                    )

                players = list(tournament.players.all())
                random.shuffle(players)  # Shuffle players randomly
                num_players = len(players)

                # Calculate players for quarters and semis
                num_quarter_matches = (num_players - 4) // 2
                players_in_quarters = num_quarter_matches * 2
                direct_to_semis = players[players_in_quarters:]
                quarter_players = players[:players_in_quarters]

                # Create quarter-final matches if there
                if quarter_players:
                    for i in range(0, len(quarter_players), 2):
                        match_id = uuid.uuid4()
                        History.objects.create(
                            match_id=match_id,
                            tournament_id=tournament,
                            user_id=quarter_players[i],
                            opponent_id=quarter_players[i + 1],
                            type_match="tournament_quarter",
                            match_number=(i // 2) + 1,
                            result_user=0,
                            result_opponent=0,
                            local_match=False,
                        )
                        History.objects.create(
                            match_id=match_id,
                            tournament_id=tournament,
                            user_id=quarter_players[i + 1],
                            opponent_id=quarter_players[i],
                            type_match="tournament_quarter",
                            match_number=(i // 2) + 1,
                            result_user=0,
                            result_opponent=0,
                            local_match=False,
                        )

                # Create semifinals matches for those who pass directly
                if direct_to_semis:
                    for i in range(0, len(direct_to_semis), 2):
                        match_id = uuid.uuid4()
                        History.objects.create(
                            match_id=match_id,
                            tournament_id=tournament,
                            user_id=direct_to_semis[i],
                            opponent_id=direct_to_semis[i + 1],
                            type_match="tournament_semi",
                            match_number=(i // 2) + 1,
                            result_user=0,
                            result_opponent=0,
                            local_match=False,
                        )
                        History.objects.create(
                            match_id=match_id,
                            tournament_id=tournament,
                            user_id=direct_to_semis[i + 1],
                            opponent_id=direct_to_semis[i],
                            type_match="tournament_semi",
                            match_number=(i // 2) + 1,
                            result_user=0,
                            result_opponent=0,
                            local_match=False,
                        )

                tournament.status = "in_progress"
                tournament.current_round = (
                    1 if quarter_players else 2
                )  # If there are no quarters, we start in semifinals
                tournament.save()

                return JsonResponse(
                    {
                        "message": "Tournament started successfully",
                        "matches": {
                            "quarter_finals": (
                                [
                                    {
                                        "match_id": str(match.match_id),
                                        "match_number": match.tournament_match_number,
                                        "player1": {
                                            "id": match.user_id.id,
                                            "username": match.user_id.username,
                                        },
                                        "player2": {
                                            "id": match.opponent_id.id,
                                            "username": match.opponent_id.username,
                                        },
                                    }
                                    for match in History.objects.filter(
                                        tournament_id=tournament,
                                        type_match="tournament_quarter",
                                    ).distinct("match_id")
                                ]
                                if quarter_players
                                else []
                            ),
                            "semi_finals": (
                                [
                                    {
                                        "match_id": str(match.match_id),
                                        "match_number": match.tournament_match_number,
                                        "player1": {
                                            "id": match.user_id.id,
                                            "username": match.user_id.username,
                                        },
                                        "player2": {
                                            "id": match.opponent_id.id,
                                            "username": match.opponent_id.username,
                                        },
                                    }
                                    for match in History.objects.filter(
                                        tournament_id=tournament,
                                        type_match="tournament_semi",
                                    ).distinct("match_id")
                                ]
                                if direct_to_semis
                                else []
                            ),
                        },
                    },
                    status=200,
                )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(
        self, _, tournament_id
    ):  # TODO: IMPLEMENT A DELETE TOURNAMENT FROM FRONTEND WHEN CANCEL TOURNAMENT IN THE JOINING WITH CODE PAGE???
        tournament = get_object_or_404(Tournaments, id=tournament_id)
        tournament.delete()
        return HttpResponse(status=204)

    def _create_next_round_matches(self, tournament, winners, next_type):
        """Create matches for the next round of a tournament"""
        for i in range(0, len(winners), 2):
            match_id = uuid.uuid4()
            History.objects.create(
                match_id=match_id,
                tournament_id=tournament,
                user_id=winners[i],
                opponent_id=winners[i + 1],
                type_match=next_type,
                match_number=(i // 2) + 1,
                result_user=0,
                result_opponent=0,
                local_match=False,
            )
            History.objects.create(
                match_id=match_id,
                tournament_id=tournament,
                user_id=winners[i + 1],
                opponent_id=winners[i],
                type_match=next_type,
                match_number=(i // 2) + 1,
                result_user=0,
                result_opponent=0,
                local_match=False,
            )

    def process_tournament_match(self, match):
        """Process tournament progression after a match is completed"""
        tournament = match.tournament_id

        # Check if all matches in current round are completed
        current_round_matches = History.objects.filter(
            tournament_id=tournament, type_match=match.type_match
        ).distinct("match_id")

        if all(
            m.result_user >= 5 or m.result_opponent >= 5 for m in current_round_matches
        ):
            winners = [
                m.user_id if m.result_user >= 5 else m.opponent_id
                for m in current_round_matches
            ]

            if match.type_match == "tournament_quarter":
                tournament.current_round = 2
                self._create_next_round_matches(tournament, winners, "tournament_semi")
            elif match.type_match == "tournament_semi":
                tournament.current_round = 3
                self._create_next_round_matches(tournament, winners, "tournament_final")
            else:  # Final
                tournament.status = "completed"

            tournament.save()
