from django.core.management.base import BaseCommand, CommandError
from bluray.models import Movie
from rottentomatoes import RT
from django.conf import settings #API KEY and SCRAPE_DAY
import re

API_KEY = getattr(settings, "API_KEY", None)
SCRAPE_DAY = getattr(settings, "SCRAPE_DAY", None)

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
		if datetime.today().isoweekday() == SCRAPE_DAY:
			print "NOT SCRAPE DAY!!"
			return

		# box_office = RT(API_KEY).movies('box_office', page_limit = 50)
		# opening = RT(API_KEY).movies('opening', page_limit = 50)
		theaters = RT(API_KEY).movies('in_theaters', page_limit = 50)

		for film in theaters:
			movie, created = Movie.objects.get_or_create(rt_id=film['id'])
			if created:
				movie.name = film['title']
				print 'Created', movie.name
				# rt object should always have a posters key. value of posters is another list
				poster = film['posters'].get('detailed', None)
				# if there is poster on rt and its not a 'default' rt poster, that implies existence of real movie poster
				if poster is not None and not re.search(".+poster_default.+", poster):
					movie.poster = poster
				movie.save()

