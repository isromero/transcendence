from django.db import models
import random
from django.contrib.auth.models import AbstractUser
from django.templatetags.static import static
import uuid


class User(AbstractUser):
    # id, username, password are inherited from AbstractUser
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar = models.URLField(
        null=True, blank=True, default=static("default_avatar.webp")
    )
    is_online = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []  # Required fields for create superuser
    deleted_user = models.BooleanField(default=False)

    """ avatar = models.URLField(
        null=True, blank=True
    )  # cambiar a una url para avatar por defecto
    email = models.EmailField(max_length=50, unique=True)
    status = models.BooleanField(default=False)
    # esto lo he añadido xq al heredar del modelo User de django, 
    # no me dejaba crear el usuario en la base de datos y hacer el login
    last_login = models.DateTimeField(null=True, blank=True) """

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
            ("match", "Local Match"),
        ],
    )
    local_match = models.BooleanField(default=True)
    tournament_id = models.ForeignKey(
        Tournaments, on_delete=models.CASCADE, null=True, blank=True
    )
    tournament_match_number = models.IntegerField(null=True, blank=True)

# TODO: (jose) borrar código comentado si no se usan los logins de 42 como filtro en el registro
# class UsedLogin(models.Model):
#     login = models.CharField(max_length=16, null=True, blank=True)
