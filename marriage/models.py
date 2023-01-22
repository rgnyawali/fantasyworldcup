from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class Player(models.Model):
	name = models.CharField(max_length=30)
	pic = models.ImageField(upload_to='images/', null=True, blank=True)
	strength = models.CharField(max_length=50, null=True, blank=True)
	weakness = models.CharField(max_length=50, null=True, blank=True)

	def __str__(self):
		return self.name


class CurrentPlayer(models.Model):
	name = models.CharField(max_length=30)

	def __str__(self):
		return self.name


class Game(models.Model):
	POINT_VALIDATOR = RegexValidator(r'^\d{0,2}[bnlxBNLX]?$','Enter your point in the format 00, N, 00L, 00B')
	
	r0=models.CharField(max_length=3, validators=[POINT_VALIDATOR], default='X')
	r1=models.CharField(max_length=3, validators=[POINT_VALIDATOR], default='X')
	r2=models.CharField(max_length=3, validators=[POINT_VALIDATOR], default='X')
	r3=models.CharField(max_length=3, validators=[POINT_VALIDATOR], default='X')
	r4=models.CharField(max_length=3, validators=[POINT_VALIDATOR], default='X')


	s0 = models.SmallIntegerField(default=0)
	s1 = models.SmallIntegerField(default=0)
	s2 = models.SmallIntegerField(default=0)
	s3 = models.SmallIntegerField(default=0)
	s4 = models.SmallIntegerField(default=0)

	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):

		return '{}-{}-{}-{}-{}'.format(self.r0, self.r1, self.r2, self.r3, self.r4)
