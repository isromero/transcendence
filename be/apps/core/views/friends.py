from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from apps.core.models import Friends, User
from apps.core.utils import serialize_friend
from apps.core.forms.friends import FriendForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name="dispatch")
class FriendsView(View):
    def get(self, _, user_id):
        user = get_object_or_404(User, id=user_id)
        friends_relations = Friends.objects.filter(user_id=user)
        return JsonResponse(
            {
                "success": True,
                "message": "Friends retrieved successfully",
                "data": [serialize_friend(relation) for relation in friends_relations],
            },
            status=200,
        )

    def post(self, request):
        try:
            data = json.loads(request.body)
            form = FriendForm(data)
            if form.is_valid():
                friend = form.save()
                return JsonResponse(
                    {
                        "success": True,
                        "message": "Friend created successfully",
                        "data": serialize_friend(friend),
                    },
                    status=201,
                )
            return JsonResponse(
                {
                    "success": False,
                    "message": "Friend creation failed",
                    "errors": form.errors,
                },
                status=400,
            )
        except json.JSONDecodeError:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Invalid JSON",
                },
                status=400,
            )

    def put(self, _, user_id, friend_id, action):
        try:
            if action not in ["accept", "reject"]:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Invalid action",
                    },
                    status=400,
                )

            friend_request = get_object_or_404(
                Friends, user_id=friend_id, friend_id=user_id, status="sent"
            )

            if action == "accept":
                friend_request.status = Friends.Status.ACCEPTED
                friend_request.save()

                # Create a reciprocal friendship record because we need to save the friendship in both directions
                Friends.objects.get_or_create(
                    user_id=user_id,
                    friend_id=friend_id,
                    defaults={"status": Friends.Status.ACCEPTED},
                )

                return JsonResponse(serialize_friend(friend_request), status=200)

            elif action == "reject":
                friend_request.status = Friends.Status.DECLINED
                friend_request.save()

                return JsonResponse(
                    {
                        "success": True,
                        "message": "Friend request declined",
                    },
                    status=200,
                )

        except json.JSONDecodeError:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Invalid JSON",
                },
                status=400,
            )

    def delete(self, _, user_id, friend_id):
        user_friends = Friends.objects.filter(user_id=user_id, friend_id=friend_id)
        friend_friends = Friends.objects.filter(user_id=friend_id, friend_id=user_id)

        deleted_count = user_friends.delete()[0] + friend_friends.delete()[0]

        if deleted_count > 0:
            return JsonResponse(
                {
                    "success": True,
                    "message": "Friend deleted successfully",
                },
                status=204,
            )
        return JsonResponse(
            {
                "success": False,
                "message": "Friend not found",
            },
            status=404,
        )
