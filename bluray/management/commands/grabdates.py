from django.core.management.base import BaseCommand, CommandError
from bluray.models import Movie
from rottentomatoes import RT
from datetime import datetime, date, timedelta
from time import sleep
import re

API_KEY = 'susmjjdwwmjwp3f437erdnd3'

'''
Scrape the dates of all movies in the database
Probably want to not scrape for movies already with dates
'''
class Command(BaseCommand):
	help = ''

	def handle(self, *args, **options):
		movies = Movie.objects.filter(released=False)
		count = 0
		for movie in movies:

			# can't make more than 5 calls a second so wait a bit
			if count % 5 == 0:
				sleep(2)

			# format movie to get rid of the translations and extra fluff
			movie_name = re.sub(r'\([^)]*\)', '', movie.name)

			try:
				rt_object = RT(API_KEY).search(movie_name)
				release_date = rt_object[0]['release_dates'].get('dvd', None)
				if release_date:
					# RT release dates look like: 2014-02-13
					movie.release = datetime.strptime(release_date, '%Y-%m-%d').date()
					movie.save()
					print movie.release, movie.name
				else:
					print "No exact date -", movie.name
			except Exception as e:
				print str(movie_name) + ": " + str(e)

			count += 1




