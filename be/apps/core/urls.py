from django.urls import path
from apps.core.views.user import UserView

urlpatterns = [
    path("", UserView.as_view(), name="users"),
    path("<int:user_id>/", UserView.as_view(), name="user"),
]
