from django.core.management.base import BaseCommand, CommandError
from bluray.models import Movie
import mechanize
from lxml import html
import time

'''
Scrape the dates of all movies in the database
Probably want to not scrape for movies already with dates
'''
class Command(BaseCommand):
	help = ''

	def handle(self, *args, **options):
		br = mechanize.Browser()
		br.set_handle_robots(False)
		br.addheaders = [('User-agent', 'Mozilla/5.0')]

		movies = Movie.objects.all()
		'''
		Since blu-ray.com doesnt give an easier way to go to a movie's link,
		google it and follow the link
		'''
		for movie in movies:
			br.open("http://google.com")
			br.select_form(nr=0)
			br.form['q'] = 'blu-ray.com %s' %movie.name
			br.submit()

			for link in br.links():
				if 'Blu-ray.com' in link.text:
					print link.url, link.text
					br.follow_link(link)
					break

			tree = html.fromstring(br.response().read())
			try:
				date = tree.xpath('//span[@style="color: #666666"]/a[@style="text-decoration: none; color: #666666"]/text()')[0]
				movie.release = datetime.datetime.strptime(date, '%b %d, %Y').date() #convert string to datetime object to a date object
				movie.save()
			except: #if exception occurs, then there is no release date
				pass

			time.sleep(10)
		return
