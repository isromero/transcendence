from django.contrib import admin
from apps.core.models import User, Friends, Stats, Tournaments, History

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
    search_fields = ("id", "username", "email")


class FriendAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "friend_id", "status")


class StatsAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "victories",
                    "defeats", "total_matches",
                    "total_tournaments", "tournaments_victories", )


class TournamentAdmin(admin.ModelAdmin):
    list_display = (
                    "id",
                    "tournament_name",
                    "start_date",
                    "end_date",
                    # "players",
                    )


class HistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "result_user", "opponent",
                    "result_opponent", "type_match", "tournament_id",
                    "position_match", "date", "position_tournament",)


admin.site.register(User, UserAdmin)
admin.site.register(Friends, FriendAdmin)
admin.site.register(Stats, StatsAdmin)
admin.site.register(Tournaments, TournamentAdmin)
admin.site.register(History, HistoryAdmin)
