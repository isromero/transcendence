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
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from apps.core.forms.tournaments import TournamentsForm


@method_decorator(csrf_exempt, name="dispatch")
class TournamentsView(View):
    def get(self, _, join_code=None):
        """Get tournament information when joining a tournament"""
        try:
            if join_code:
                tournament = get_object_or_404(Tournaments, join_code=join_code)

                if tournament.status == "in_progress":
                    matches = History.objects.filter(tournament_id=tournament)

                    if tournament.max_players == 4:
                        semi_matches = matches.filter(
                            type_match="tournament_semi"
                        ).distinct("tournament_match_number")

                        final_matches = matches.filter(
                            type_match="tournament_final"
                        ).distinct("tournament_match_number")

                        semis_finished = all(
                            max(
                                matches.filter(match_id=m.match_id).values_list(
                                    "result_user", flat=True
                                )
                            )
                            >= 5
                            for m in semi_matches
                        )

                        finals_finished = (
                            all(
                                max(
                                    matches.filter(match_id=m.match_id).values_list(
                                        "result_user", flat=True
                                    )
                                )
                                >= 5
                                for m in final_matches
                            )
                            if final_matches.exists()
                            else False
                        )

                        if semis_finished and finals_finished:
                            tournament.status = "completed"
                            tournament.save()

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

            display_name = data.get("display_name")

            user = User.objects.get(id=request.user.id)
            user.tournament_display_name = display_name
            user.save()

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
            join_code = data.get("join_code")
            tournament_id = data.get("tournament_id")

            if not tournament_id or not action:
                return create_response(
                    error="Tournament ID and action are required", status=400
                )

            tournament = get_object_or_404(Tournaments, id=tournament_id)

            if action == "join":

                display_name = data.get("display_name")

                # Check if the display_name is already in use in this tournament
                if tournament.players.filter(
                    tournament_display_name=display_name
                ).exists():
                    display_name = (
                        request.user.username
                    )  # Use the username if the display_name is already in use
                    return create_response(
                        error=f"Display name '{data.get('display_name')}' is already taken. Your username '{display_name}' will be used instead.",
                        status=400,
                    )

                user = User.objects.get(id=request.user.id)
                user.tournament_display_name = display_name
                user.save()

                if tournament.join_code != join_code:
                    return create_response(error="Invalid join code", status=400)

                if (
                    tournament.players.count() >= tournament.max_players
                    and request.user not in tournament.players.all()
                ):
                    return create_response(error="Tournament is full", status=400)

                tournament.players.add(request.user)
                if (
                    tournament.players.count() == tournament.max_players
                    and tournament.status == "pending"
                ):
                    tournament.status = "ready"
                tournament.save()
                return create_response(
                    message=f"Joined tournament successfully with display name '{display_name}'",
                    status=200,
                )

            elif action == "leave":
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

                # Get players in order of joining this specific tournament
                players = list(
                    tournament.players.through.objects.filter(tournaments=tournament)
                    .order_by("id")
                    .values_list("user", flat=True)
                )
                players = [User.objects.get(id=player_id) for player_id in players]

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

                return create_response(
                    data=serialize_tournament(tournament),
                    message="Next round generated successfully",
                    status=200,
                )

            else:
                return create_response(error="Unknown action", status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request):
        """Deletes a tournament"""
        data = json.loads(request.body)
        tournament_id = data.get("tournament_id")
        tournament = get_object_or_404(Tournaments, id=tournament_id)
        tournament.delete()
        return HttpResponse(status=204)

    def _create_match(
        self, tournament, user1, user2, type_match, match_id, match_number
    ):
        existing_match = History.objects.filter(
            tournament_id=tournament,
            type_match=type_match,
            tournament_match_number=match_number,
        ).first()

        if existing_match:
            return

        History.objects.create(
            match_id=match_id,
            tournament_id=tournament,
            user_id=user1,
            opponent_id=user2,
            type_match=type_match,
            tournament_match_number=match_number,
            result_user=0,
            result_opponent=0,
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
        )

    def _create_next_round_matches(self, tournament, winners, next_type):
        # Check if there are already matches for this round
        existing_matches = (
            History.objects.filter(tournament_id=tournament, type_match=next_type)
            .values("tournament_match_number")
            .distinct()
        )

        if existing_matches.exists():
            return

        # For finals, we need to ensure that only one match is created
        if next_type == "tournament_final":
            match_id = uuid.uuid4()

            self._create_match(
                tournament,
                winners[0],
                winners[1],
                next_type,
                match_id,
                1,
            )
        else:
            for i in range(0, len(winners), 2):
                match_id = uuid.uuid4()
                match_number = (i // 2) + 1

                self._create_match(
                    tournament,
                    winners[i],
                    winners[i + 1],
                    next_type,
                    match_id,
                    match_number,
                )
