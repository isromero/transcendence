from django.http import JsonResponse, HttpResponse
from django.views import View
from django.shortcuts import get_object_or_404
from apps.core.models import Tournaments, History
from apps.core.utils import serialize_tournament, serialize_tournaments
from apps.core.forms.tournaments import TournamentsForm, TournamentsPutForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name="dispatch")
class TournamentsView(View):
    def get(self, _, tournament_id=None):
        if tournament_id:
            tournament = get_object_or_404(Tournaments, id=tournament_id)

            return JsonResponse(serialize_tournament(tournament), status=200)
        else:
            tournaments = Tournaments.objects.all()

            return JsonResponse(
                {
                    "data": [
                        serialize_tournaments(tournament) for tournament in tournaments
                    ]
                },
                status=200,
            )

    def post(self, request):
        try:
            data = json.loads(request.body)
            form = TournamentsForm(data)
            if form.is_valid():
                tournament = form.save()
                return JsonResponse(serialize_tournament(tournament), status=201)
            return JsonResponse({"errors": form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def put(self, request, tournament_id):
        tournament = get_object_or_404(Tournaments, id=tournament_id)
        try:
            data = json.loads(request.body)
            form = TournamentsPutForm(data, instance=tournament)
            if form.is_valid():
                user = form.save()
                return JsonResponse(serialize_tournament(tournament), status=200)
            return JsonResponse({"errors": form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def delete(self, _, tournament_id):
        tournament = get_object_or_404(Tournaments, id=tournament_id)
        tournament.delete()
        return HttpResponse(status=204)
