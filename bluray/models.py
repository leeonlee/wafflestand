from django.db import models
from django.contrib.auth.models import User #allow movie to keep track of users
from django import forms

# Create your models here.
class Movie(models.Model):
	name = models.CharField(max_length=100)
	release = models.DateField(null=True, blank=True)
	tracking = models.ManyToManyField(User)
	released = models.BooleanField(default=False)
	poster = models.CharField(max_length=100, null=True, blank=True)

	#basically the toString
	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ('name',)

class LoginForm(forms.Form):
	username = forms.CharField(label=('Username'), max_length=30)
	password = forms.CharField(label=('Password'), widget=forms.PasswordInput(render_value=False), max_length=30)
