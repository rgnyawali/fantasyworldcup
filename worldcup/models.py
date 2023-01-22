from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings

# Create your models here.

GROUP_CHOICES = tuple(zip(list('ABCDEFGH'),list('ABCDEFGH')))
MATCH_TYPE = (
    ('group', 'Group Match'),
    ('grp1','Group Round 1'),
    ('grp2', 'Group Round 2'),
    ('grp3','Group Round 3'),
    ('r16', 'Round of 16'),
    ('qf', 'Quarter Final'),
    ('sf', 'Semi Final'),
    ('f', 'Final'),
    )

class Team(models.Model):
    name = models.CharField(max_length=30)
    shortname = models.CharField(max_length=3)
    group = models.CharField(max_length=1, choices=GROUP_CHOICES)
    played = models.PositiveSmallIntegerField(default=0)
    won = models.PositiveSmallIntegerField(default=0)
    draw = models.PositiveSmallIntegerField(default=0)
    lost = models.PositiveSmallIntegerField(default=0)
    gf = models.PositiveSmallIntegerField(default=0)
    ga = models.PositiveSmallIntegerField(default=0)
    gd = models.SmallIntegerField(default=0)
    points = models.PositiveSmallIntegerField(default=0)
    flag = models.ImageField(upload_to='images/', null=True)

    def __str__(self):
        return self.name

class Match(models.Model):
    SCORE_REGEX = RegexValidator(r'^\d{1,2}-\d{1,2}$', 'Please enter the score in format 00-00 or 0-0')
    teamA = models.ForeignKey('Team', related_name='teamA', on_delete=models.CASCADE)
    teamB = models.ForeignKey('Team', related_name='teamB', on_delete=models.CASCADE)
    date = models.DateTimeField()
    actual_score = models.CharField(max_length=5, validators=[SCORE_REGEX], blank=True, null=True)
    user_score = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Score', related_name='score_user')
    match_type = models.CharField(max_length=5, choices=MATCH_TYPE)

    def __str__(self):
        return ('{} vs {}'.format(self.teamA, self.teamB))


class KnockOutTeamSelection(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    qf1 = models.ForeignKey('Team', related_name='qf1', on_delete=models.CASCADE)
    qf2 = models.ForeignKey('Team', related_name='qf2', on_delete=models.CASCADE)
    qf3 = models.ForeignKey('Team', related_name='qf3', on_delete=models.CASCADE)
    qf4 = models.ForeignKey('Team', related_name='qf4', on_delete=models.CASCADE)
    qf5 = models.ForeignKey('Team', related_name='qf5', on_delete=models.CASCADE)
    qf6 = models.ForeignKey('Team', related_name='qf6', on_delete=models.CASCADE)
    qf7 = models.ForeignKey('Team', related_name='qf7', on_delete=models.CASCADE)
    qf8 = models.ForeignKey('Team', related_name='qf8', on_delete=models.CASCADE)
    sf1 = models.ForeignKey('Team', related_name='sf1', on_delete=models.CASCADE)
    sf2 = models.ForeignKey('Team', related_name='sf2', on_delete=models.CASCADE)
    sf3 = models.ForeignKey('Team', related_name='sf3', on_delete=models.CASCADE)
    sf4 = models.ForeignKey('Team', related_name='sf4', on_delete=models.CASCADE)
    f1 = models.ForeignKey('Team', related_name='f1', on_delete=models.CASCADE)
    f2 = models.ForeignKey('Team', related_name='f2', on_delete=models.CASCADE)
    champion = models.ForeignKey('Team', related_name='champion', on_delete=models.CASCADE)
    qfpoints = models.PositiveSmallIntegerField(default=0)
    sfpoints = models.PositiveSmallIntegerField(default=0)
    fpoints = models.PositiveSmallIntegerField(default=0)
    champpoints = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return ("{}::{}".format(self.owner, "Knock Out Team Selection"))


class Score(models.Model):
    SCORE_REGEX = RegexValidator(r'^\d{1,2}-\d{1,2}$', 'Please enter the score in format 00-00 or 0-0')
    myscore = models.CharField(max_length=5, validators=[SCORE_REGEX], help_text='Enter your score in format 0-0 or 00-00')
    mymatch = models.ForeignKey(Match, on_delete=models.CASCADE)
    mypoints = models.PositiveSmallIntegerField(default=0)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "{}:{}:{}".format(self.owner, self.mymatch, self.myscore)


class LeaderBoard(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    points = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return ("{}: {}".format(self.owner, self.points))


class Comment(models.Model):
    text = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if len(self.text) < 15: return self.text
        return self.text[:11] + " ..."






