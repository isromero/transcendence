from django.contrib import admin
from apps.core.models import User, Friends, Tournaments, History


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")
    search_fields = ("id", "username")


class FriendAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "friend_id", "status")


class TournamentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tournament_name",
        "start_date",
        "end_date",
    )


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "match_id",
        "date",
        "user_id",
        "result_user",
        "opponent_id",
        "result_opponent",
        "type_match",
        "tournament_id",
        "tournament_match_number",
    )


admin.site.register(User, UserAdmin)
admin.site.register(Friends, FriendAdmin)
admin.site.register(Tournaments, TournamentAdmin)
