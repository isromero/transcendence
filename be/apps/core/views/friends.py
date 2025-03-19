from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from apps.core.models import Friends, User
from apps.core.utils import serialize_friend
from apps.core.forms.friends import FriendForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from apps.core.utils import create_response, handle_form_errors


@method_decorator(csrf_exempt, name="dispatch")
class FriendsView(View):
    def get(self, _, user_id):
        try:
            user = get_object_or_404(User, id=user_id)
            friends_relations = Friends.objects.filter(user_id=user)
            return create_response(
                data=[serialize_friend(relation) for relation in friends_relations],
                message="Friends retrieved successfully",
            )
        except Exception as e:
            return create_response(error=str(e), status=400)

    def post(self, request):
        try:
            data = json.loads(request.body)
            form = FriendForm(data)

            if not form.is_valid():
                return handle_form_errors(form)

            friend = form.save()
            return create_response(
                data=serialize_friend(friend),
                message="Friend created successfully",
                status=201,
            )
        except json.JSONDecodeError:
            return create_response(error="Invalid JSON", status=400)

    def put(self, _, user_id, friend_id, action):
        try:
            if action not in ["accept", "reject"]:
                return create_response(error="Invalid action", status=400)

            friend_request = get_object_or_404(
                Friends, user_id=friend_id, friend_id=user_id, status="sent"
            )

            if action == "accept":
                friend_request.status = Friends.Status.ACCEPTED
                friend_request.save()

                # Create a reciprocal friendship record
                Friends.objects.get_or_create(
                    user_id=user_id,
                    friend_id=friend_id,
                    defaults={"status": Friends.Status.ACCEPTED},
                )

                return create_response(
                    data=serialize_friend(friend_request),
                    message="Friend request accepted",
                )

            elif action == "reject":
                friend_request.status = Friends.Status.DECLINED
                friend_request.save()

                return create_response(message="Friend request declined")

        except Exception as e:
            return create_response(error=str(e), status=400)

    def delete(self, _, user_id, friend_id):
        user_friends = Friends.objects.filter(user_id=user_id, friend_id=friend_id)
        friend_friends = Friends.objects.filter(user_id=friend_id, friend_id=user_id)

        deleted_count = user_friends.delete()[0] + friend_friends.delete()[0]

        if deleted_count > 0:
            return create_response(message="Friend deleted successfully", status=204)
        return create_response(error="Friend not found", status=404)
