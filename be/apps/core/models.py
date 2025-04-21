from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    # id, username, password are inherited from AbstractUser
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default="/images/default_avatar.webp",
    )
    last_activity = models.DateTimeField(default=timezone.now)
    deleted_user = models.BooleanField(default=False)

    tournament_display_name = models.CharField(max_length=150, null=True, blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []  # Required fields for create superuser
    deleted_user = models.BooleanField(default=False)

    @property
    def is_online(self):
        if not self.last_activity:
            return False
        return (timezone.now() - self.last_activity).seconds < 45

    def save(self, *args, **kwargs):
        if self._state.adding and not self.tournament_display_name:
            self.tournament_display_name = self.username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Friends(models.Model):
    class Status(models.TextChoices):
        DECLINED = "declined"
        ACCEPTED = "accepted"
        SENT = "sent"

    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friends_as_user"
    )
    friend_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friends_as_friend"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=Status.choices, default=Status.SENT)


class Tournaments(models.Model):
    id = models.AutoField(primary_key=True)
    join_code = models.CharField(max_length=6, unique=True)
    tournament_name = models.CharField(max_length=50)
    start_date = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField(auto_now=True)
    players = models.ManyToManyField(User, related_name="tournaments_name")
    current_round = models.IntegerField(default=1)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("ready", "Ready"),
            ("in_progress", "In Progress"),
            ("completed", "Completed"),
        ],
        default="pending",
    )
    max_players = models.IntegerField(default=8)


class History(models.Model):
    id = models.AutoField(primary_key=True)
    match_id = models.UUIDField(default=None, null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_history"
    )
    result_user = models.IntegerField(default=0)
    opponent_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="opponent_history"
    )
    result_opponent = models.IntegerField(default=0)
    type_match = models.CharField(
        max_length=50,
        choices=[
            ("tournament_quarter", "Tournament Quarter Finals"),
            ("tournament_semi", "Tournament Semi Finals"),
            ("tournament_final", "Tournament Finals"),
            ("local", "Local Match"),
            ("multiplayer", "Multiplayer Match"),
        ],
    )
    tournament_id = models.ForeignKey(
        Tournaments, on_delete=models.CASCADE, null=True, blank=True
    )
    tournament_match_number = models.IntegerField(null=True, blank=True)
