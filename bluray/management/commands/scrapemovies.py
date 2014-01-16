from django.core.management.base import BaseCommand, CommandError
from bluray.models import Movie
import mechanize
from lxml import html

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
		br = mechanize.Browser()
		br.set_handle_robots(False)
		br.addheaders = [('User-agent', 'Mozilla/5.0')]

		br.open('http://www.rottentomatoes.com/movie/box-office/')
		tree = html.fromstring(br.response().read()) #pass in the html

		'''
		Returns a list of all movie titles in the page
		//td[@class="left"] = select all td elements in class left
		/a = select all a elements that are children of what comes before it
		/text() = get text ex. <a href=''>text</a>
		http://www.w3schools.com/xpath/xpath_syntax.asp
		'''
		movies = tree.xpath('//td[@class="left"]/a/text()')

		#create movie objects for all of the movie titles. if it already exists, nothing happens
		for movie in movies:
			Movie.objects.get_or_create(name=movie)
