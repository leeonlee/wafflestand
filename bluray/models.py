from django.db import models
from django.contrib.auth.models import User #allow movie to keep track of users

# Create your models here.
class Movie(models.Model):
	name = models.CharField(max_length=100)
	release = models.DateField(null=True, blank=True)
	tracking = models.ManyToManyField(User)
	released = models.BooleanField(default=False)

	#basically the toString
	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ('name',)
