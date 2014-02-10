from django.core.management.base import BaseCommand, CommandError
from bluray.models import Movie
from rottentomatoes import RT
import re

API_KEY = 'susmjjdwwmjwp3f437erdnd3'

'''
Method to generate new movie objects
Probably should scrape new releases
or maybe http://www.rottentomatoes.com/movie/box-office/
if they're out in theaters still then they probably dont have blu ray out
run once a week?
'''
class Command(BaseCommand):
	help = ''

	def handle(self, *args, **options):
		# box_office = RT(API_KEY).movies('box_office', page_limit = 50)
		# opening = RT(API_KEY).movies('opening', page_limit = 50)
		theaters = RT(API_KEY).movies('in_theaters', page_limit = 50)

		for film in theaters:
			movie, created = Movie.objects.get_or_create(name=film['title'])
			if created:
				print 'Created', movie.name
				poster = film['posters'].get('detailed', None)
				if poster is not None and not re.search(".+poster_default.+", poster):
					movie.poster = poster
					movie.save()

