from django.core.management.base import BaseCommand, CommandError
from bluray.models import Movie
from rottentomatoes import RT
from datetime import datetime
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
			# can't make more than 5 calls a second
			if count % 5 == 0:
				sleep(2)
			movie_name = re.sub(r'\([^)]*\)', '', movie.name)
			try:
				rt_object = RT(API_KEY).search(movie_name)
				release_date = rt_object[0]['release_dates'].get('dvd', None)
				if release_date:
					rd = datetime.strptime(release_date, '%Y-%m-%d')
					movie.release = datetime.strptime(rd.strftime("%B %d, %Y"), "%B %d, %Y")
					print movie.release, movie.name
				else:
					print "No exact date -", movie.name
				movie.save()
			except Exception as e:
				print str(movie_name) + ": " + str(e)
			count += 1




