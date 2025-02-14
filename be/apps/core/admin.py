from django.contrib import admin
from apps.core.models import User, Friends, Tournaments, History

# Register your models here.

# class AuditLog(admin.ModelAdmin):
#     list_display = ("id", "entity_name", "record_id", "action",
#                     "old_data", "new_data", "timestamp",
#                     "entity_id",)

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
    search_fields = ("id", "username", "email")


class FriendAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "friend_id", "status")


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
admin.site.register(Tournaments, TournamentAdmin)
admin.site.register(History, HistoryAdmin)
