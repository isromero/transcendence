from django.http import JsonResponse, HttpResponse
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
                return create_response(
                    data=serialize_tournament(tournament),
                    message="Tournament retrieved successfully",
                    status=200,
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

    def put(self, request):
        """Handles join, leave, start and next_round actions"""
        try:
            data = json.loads(request.body)
            action = data.get("action")
            tournament_id = data.get("tournament_id")

            if not tournament_id or not action:
                return create_response(
                    error="Tournament ID and action are required", status=400
                )

            tournament = get_object_or_404(Tournaments, id=tournament_id)

            if action == "join":
                join_code = data.get("join_code")
                if tournament.join_code != join_code:
                    return create_response(error="Invalid join code", status=400)

                if (
                    tournament.players.count() >= tournament.max_players
                    and request.user not in tournament.players.all()
                ):
                    return create_response(error="Tournament is full", status=400)

                tournament.players.add(request.user)
                if tournament.players.count() == tournament.max_players:
                    tournament.status = "ready"
                tournament.save()
                return create_response(
                    message="Joined tournament successfully", status=200
                )

            elif action == "leave":
                join_code = data.get("join_code")
                if tournament.join_code != join_code:
                    return create_response(error="Invalid join code", status=400)

                # Uncomment this if we don't want the user to leave, but we can't force that... so... not useful
                # if tournament.status not in ["pending", "ready"]:
                #     return create_response(
                #         error="You can't leave started tournaments", status=400
                #     )

                tournament.players.remove(request.user)

                # If a player leaves, we need to check if we need to change the status
                current_players = tournament.players.count()
                if tournament.status == "ready" and current_players not in [4, 8]:
                    tournament.status = "pending"

                tournament.save()
                return create_response(
                    message="Leaved the tournament successfully", status=200
                )

            elif action == "start":
                if tournament.status != "ready" or tournament.players.count() not in [
                    4,
                    8,
                ]:
                    return create_response(
                        error="Tournament is not ready to start", status=400
                    )

                players = list(tournament.players.all())
                random.shuffle(players)
                num_players = len(players)
                num_quarter_matches = (num_players - 4) // 2
                players_in_quarters = num_quarter_matches * 2
                direct_to_semis = players[players_in_quarters:]
                quarter_players = players[:players_in_quarters]

                if quarter_players:
                    for i in range(0, len(quarter_players), 2):
                        match_id = uuid.uuid4()
                        self._create_match(
                            tournament,
                            quarter_players[i],
                            quarter_players[i + 1],
                            "tournament_quarter",
                            match_id,
                            (i // 2) + 1,
                        )

                if direct_to_semis:
                    for i in range(0, len(direct_to_semis), 2):
                        match_id = uuid.uuid4()
                        self._create_match(
                            tournament,
                            direct_to_semis[i],
                            direct_to_semis[i + 1],
                            "tournament_semi",
                            match_id,
                            (i // 2) + 1,
                        )

                tournament.status = "in_progress"
                tournament.current_round = 1 if quarter_players else 2
                tournament.save()

                return create_response(
                    data=serialize_tournament(tournament),
                    message="Tournament started successfully",
                    status=200,
                )

            elif action == "next_round":
                if tournament.status != "in_progress":
                    return create_response(
                        error="Tournament is not in progress", status=400
                    )

                round_type_map = {
                    1: "tournament_quarter",
                    2: "tournament_semi",
                    3: "tournament_final",
                }

                next_round_map = {
                    1: (2, "tournament_semi"),
                    2: (3, "tournament_final"),
                }

                current_type = round_type_map.get(tournament.current_round)
                if not current_type:
                    return create_response(error="Invalid current round", status=400)

                winners = []
                matches = History.objects.filter(
                    tournament_id=tournament, type_match=current_type
                ).distinct("match_id")

                for match in matches:
                    if match.result_user >= 5:
                        winners.append(match.user_id)
                    else:
                        winners.append(match.opponent_id)

                if tournament.current_round in next_round_map:
                    next_round, next_type = next_round_map[tournament.current_round]
                    self._create_next_round_matches(tournament, winners, next_type)
                    tournament.current_round = next_round
                    tournament.save()
                else:
                    # If we are in the final, we don't mark "completed" until the match is played

                    if match.type_match == "tournament_final":
                        all_final_matches = History.objects.filter(
                            tournament_id=tournament.id, type_match="tournament_final"
                        ).distinct("match_id")

                        final_matches_finished = all(
                            m.result_user is not None for m in all_final_matches
                        )

                        if final_matches_finished:
                            tournament.status = "completed"
                            tournament.save()

                return create_response(
                    data=serialize_tournament(tournament),
                    message="Next round generated successfully",
                    status=200,
                )

            else:
                return create_response(error="Unknown action", status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, _, tournament_id):
        """Deletes a tournament"""
        tournament = get_object_or_404(Tournaments, id=tournament_id)
        tournament.delete()
        return HttpResponse(status=204)

    def _create_match(
        self, tournament, user1, user2, type_match, match_id, match_number
    ):
        History.objects.create(
            match_id=match_id,
            tournament_id=tournament,
            user_id=user1,
            opponent_id=user2,
            type_match=type_match,
            tournament_match_number=match_number,
            result_user=0,
            result_opponent=0,
            local_match=False,
        )
        History.objects.create(
            match_id=match_id,
            tournament_id=tournament,
            user_id=user2,
            opponent_id=user1,
            type_match=type_match,
            tournament_match_number=match_number,
            result_user=0,
            result_opponent=0,
            local_match=False,
        )

    def _create_next_round_matches(self, tournament, winners, next_type):
        for i in range(0, len(winners), 2):
            match_id = uuid.uuid4()
            self._create_match(
                tournament,
                winners[i],
                winners[i + 1],
                next_type,
                match_id,
                (i // 2) + 1,
            )
