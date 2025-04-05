from django.views import View
from apps.core.models import Friends
from apps.core.utils import serialize_friend
from apps.core.forms.friends import FriendForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from apps.core.utils import create_response, handle_form_errors


@method_decorator(csrf_exempt, name="dispatch")
class FriendsView(View):
    def get(self, request):
        try:
            user = request.user
            action = request.GET.get("action")
            if action == "requests":
                # Get pending friend requests
                friend_requests = Friends.objects.filter(
                    friend_id=user, status=Friends.Status.SENT
                )
                return create_response(
                    data=[serialize_friend(relation) for relation in friend_requests],
                    message="Friend requests retrieved successfully",
                )
            else:
                # Get accepted friends
                friends = Friends.objects.filter(
                    user_id=user, status=Friends.Status.ACCEPTED
                )
                return create_response(
                    data=[serialize_friend(relation) for relation in friends],
                    message="Friends retrieved successfully",
                )
        except Exception as e:
            return create_response(error=str(e), status=400)

    def post(self, request):
        try:
            data = json.loads(request.body)
            form = FriendForm(data, user=request.user)

            if not form.is_valid():
                return handle_form_errors(form)

            friend = form.save()
            return create_response(
                data=serialize_friend(friend),
                message="Friend request sent successfully",
                status=201,
            )
        except json.JSONDecodeError:
            return create_response(error="Invalid JSON", status=400)

    def put(self, request, user_id, action):
        try:
            friend_id = request.user.id

            # Search for the friend request
            friend_request = Friends.objects.filter(
                user_id=user_id, friend_id=friend_id, status=Friends.Status.SENT
            ).first()

            if not friend_request:
                return create_response(error="Friend request not found", status=404)

            if action == "accept":
                # Update the original request
                friend_request.status = Friends.Status.ACCEPTED
                friend_request.save()

                # Create the reciprocal relationship
                Friends.objects.create(
                    user_id_id=friend_id,  # Current user
                    friend_id_id=user_id,  # User who sent the request
                    status=Friends.Status.ACCEPTED,
                )
                return create_response(
                    data=serialize_friend(friend_request),
                    message="Friend request accepted successfully",
                )
            elif action == "reject":
                friend_request.status = Friends.Status.DECLINED
                friend_request.save()
                return create_response(message="Friend request rejected successfully")
            else:
                return create_response(error="Invalid action", status=400)

        except Exception as e:
            return create_response(error=str(e), status=400)

    def delete(self, _, user_id, friend_id):
        user_friends = Friends.objects.filter(user_id=user_id, friend_id=friend_id)
        friend_friends = Friends.objects.filter(user_id=friend_id, friend_id=user_id)

        deleted_count = user_friends.delete()[0] + friend_friends.delete()[0]

        if deleted_count > 0:
            return create_response(message="Friend deleted successfully", status=204)
        return create_response(error="Friend not found", status=404)
