from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=30)
    played = models.PositiveSmallIntegerField(default=0)
    won = models.PositiveSmallIntegerField(default=0)
    lost = models.PositiveSmallIntegerField(default=0)
    point = models.PositiveSmallIntegerField(default=0)
    form = models.TextField()
    rank = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

class Match(models.Model):
    SCORE_REGEX = RegexValidator(r'^\d{1,2}-\d{1,2}$', 'Please enter the score in format 00-00 or 0-0')
    player1 = models.ForeignKey('Player', related_name='Player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey('Player', related_name='Player2', on_delete=models.CASCADE)
    score1 = models.CharField(max_length=5, validators=[SCORE_REGEX], blank=True, null=True)
    score2 = models.CharField(max_length=5, validators=[SCORE_REGEX], blank=True, null=True)
    score3 = models.CharField(max_length=5, validators=[SCORE_REGEX], blank=True, null=True)
    score4 = models.CharField(max_length=5, validators=[SCORE_REGEX], blank=True, null=True)
    score5 = models.CharField(max_length=5, validators=[SCORE_REGEX], blank=True, null=True)
    date = models.DateTimeField()
    venue = models.CharField(max_length=30)

    p1s1 = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    p1s2 = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    p1s3 = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    p1s4 = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    p1s5 = models.PositiveSmallIntegerField(default=0, blank=True, null=True)

    p2s1 = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    p2s2 = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    p2s3 = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    p2s4 = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    p2s5 = models.PositiveSmallIntegerField(default=0, blank=True, null=True)

    winner = models.ForeignKey('Player',related_name='winner', on_delete=models.CASCADE)
    winrate = models.CharField(max_length=3)

    def __str__(self):
        return '{} vs {}'.format(self.player1, self.player2)
