from django.db import models

# Create your models here.
class Mes(models.Model):
    nombre = models.CharField(primary_key=True, max_length=255)
    numero = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mes'
		

class Country(models.Model):
	ioc = models.CharField(primary_key=True, max_length=3)
	name = models.CharField(max_length=255)


class Player(models.Model):
	class Handedness(models.TextChoices):
		LEFT = "L"
		RIGHT = "R"
		AMBI = "A"
		UNKNOWN = "U"

	name = models.CharField(max_length=255, db_index=True)
	last_name = models.CharField(max_length=255, db_index=True)
	dob = models.DateField(null=True, db_index=True)
	handedness = models.CharField(max_length=1, choices=Handedness.choices, default=Handedness.UNKNOWN)
	ioc = models.ForeignKey("Country", on_delete=models.SET_NULL, null=True, db_index=True)


class Tournament(models.Model):
	class Surface(models.TextChoices):
		HARD = "Hard"
		CLAY = "Clay"
		GRASS = "Grass"
		CARPET = "Carpet"
		UNKNOWN = "Unknown"
		
	id = models.CharField(max_length=255, primary_key=True)
	name = models.CharField(max_length=255, null=False)
	start_date = models.DateField(db_index=True)
	level = models.CharField(max_length=1, null=False)
	surface = models.CharField(max_length=10, choices=Surface.choices, null=False)



class PlayerMatchStats(models.Model):
	class Meta:
		unique_together = (("match", "player"),)
	class Result(models.TextChoices):
		WINNER = "W"
		LOSER = "L"
	match = models.ForeignKey("Match", on_delete=models.CASCADE, null=False, db_index=True)
	player = models.ForeignKey("Player", on_delete=models.CASCADE, null=False, db_index=True)
	result = models.CharField(max_length=1, choices=Result.choices, null=False, db_index=True)
	height = models.PositiveSmallIntegerField(null=True)


class Match(models.Model):
	tournament = models.ForeignKey("Tournament", on_delete=models.CASCADE, null=False, db_index=True)
	match_num = models.IntegerField(db_index=True)
	players = models.ManyToManyField("Player", through="PlayerMatchStats")
	best_of = models.PositiveSmallIntegerField()
	round = models.CharField(max_length=10, null=False)
	score = models.CharField(max_length=255, null=False)

class Ranking(models.Model):
	player = models.ForeignKey("Player", on_delete=models.CASCADE, db_index=True)
	date = models.DateField(db_index=True)
	rank = models.IntegerField()
	points = models.IntegerField()

