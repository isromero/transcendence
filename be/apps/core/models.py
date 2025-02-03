from django.db import models
from django.core.validators import MinLengthValidator


class User(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.CharField(
        max_length=50, unique=True, validators=[MinLengthValidator(3)]
    )
    password = models.CharField(max_length=128, validators=[MinLengthValidator(8)])
    avatar = models.URLField(
        null=True, blank=True
    )  # cambiar a una url para avatar por defecto
    email = models.EmailField(max_length=50, unique=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Friends(models.Model):
    STATUS_CHOICES = [
        (0, "declined"),
        (1, "accepted"),
        (2, "sent"),
    ]
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    friend_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_friends"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES)


class Stats(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    victories = models.IntegerField(default=0)
    defeats = models.IntegerField(default=0)
    total_matches = models.IntegerField(default=0)
    total_tournaments = models.IntegerField(default=0)
    tournaments_victories = models.IntegerField(default=0)


class Tournaments(models.Model):
    id = models.AutoField(primary_key=True)
    tournament_name = models.CharField(max_length=50)
    start_date = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField(auto_now=True)
    players = models.ManyToManyField(User, related_name="tournaments_name")


class History(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_history"
    )
    result_user = models.IntegerField()
    opponent = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="opponent"
    )
    result_opponent = models.IntegerField()
    type_match = models.CharField(max_length=50)  # match o tournament_example
    tournament_id = models.ForeignKey(Tournaments, on_delete=models.CASCADE)
    position_match = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    position_tournament = models.IntegerField()
