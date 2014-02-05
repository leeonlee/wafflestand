from django.core.management.base import BaseCommand, CommandError
from bluray.models import Movie
import datetime

'''
Checks the release dates of every movie in the database by subtracting future release date from today
Should probably check only movies that have not been released
Maybe have a boolean field or a separate model for released movies?
'''
class Command(BaseCommand):
	help = ''

	def handle(self, *args, **options):
		movies = Movie.objects.filter(released=False)
		release_today = []
		today = datetime.date.today()
		for movie in movies:
			print 'Checking', movie.name
			if movie.release != None:
				if movie.release - today <= datetime.timedelta(0):
					release_today.append(movie)
					movie.released = True
					movie.save()

		'''
		Should either store release_today and send emails later or start sending out emails immediately
		'''
		email_list = []
		for movie in release_today:
			email_list.extend([user.email for user in movie.tracking.all() if user.email not in email_list])
			movie.tracking.clear()
			print email_list
		#do something with the emails
