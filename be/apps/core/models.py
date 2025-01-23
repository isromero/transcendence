from django.db import models

# Create your models here.

class Users(models.Model):
	id = models.AutoField(primary_key=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	username = models.CharField(max_length=50, unique=True)
	password = models.CharField(max_length=50)
	avatar = models.URLField(null=True) #cambiar a una url para avatar por defecto
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
	user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
	friend_id = models.OneToOneField(Users, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(choices=STATUS_CHOICES)

class Stats(models.Model):
	id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
	victories = models.IntegerField(default=0)
	defeats = models.IntegerField(default=0)
	total_matches = models.IntegerField(default=0)

class History(models.Model):
	id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
	result_user = models.IntegerField()
	opponent = models.ForeignKey(Users, on_delete=models.CASCADE)
	result_opponent = models.IntegerField()
	type_match = models.CharField(max_length=50) #match o tournament_example

	tournament_id = models.ForeignKey(Users, on_delete=models.CASCADE)
	position_match = models.IntegerField()
	date = models.DateTimeField(auto_now_add=True)
	position_tourmanent = models.IntegerField()

class Tournaments(models.Model):
	id = models.AutoField(primary_key=True)
	tournament_name = models.CharField(max_length=50)
	start_date = models.DateTimeField(auto_now_add=True)
	end_date = models.DateTimeField(auto_now_add=True)
	players = models.ManyToManyField(Users, related_name="tournaments_name")