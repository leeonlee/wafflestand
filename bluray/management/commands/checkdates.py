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
		movies = Movie.objects.all()
		release_today = []
		today = datetime.date.today()
		for movie in movies:
			if movie.release != None:
				print movie.release - today, movie.name
				if movie.release - today <= datetime.timedelta(0):
					release_today.append(movie)

		'''
		Should either store release_today and send emails later or start sending out emails immediately
		'''


