from django.core.management.base import BaseCommand, CommandError
from bluray.models import Movie
from lxml import html
import time, re
from datetime import datetime
import requests

'''
Scrape the dates of all movies in the database
Probably want to not scrape for movies already with dates
'''
class Command(BaseCommand):
	help = ''

	def handle(self, *args, **options):
		movies = Movie.objects.filter(released=False)
		for movie in movies:
			#Remove translated titles (usually in parentheses) because it screws with search
			name_to_url = re.sub(r'\([^)]*\)', '', movie.name).replace(' ', '+')
			name_to_url = "https://www.google.com/search?q=videoeta+" + name_to_url
			page = requests.get(name_to_url)
			tree = html.fromstring(page.text)

			#example link '/url?q=http://videoeta.com/movie/138795/frozen/&sa=U&ei=bwTjUsmdMenNsQSLqoKgBg&ved=0CBsQFjAA&usg=AFQjCNFM8VRTW1cgtwEGibllvbKNdT4_dA'
			links = tree.xpath('//h3[@class="r"]/a')
			link_with_movie = ''
			for link in links:
				if 'movie' in link.attrib['href']:
					link_with_movie = link.attrib['href']
					break
			print link_with_movie
			page = requests.get(re.search('q=(.*)&s', link_with_movie).group(1).replace('%3F', '?').replace('%3D', '='))

			tree = html.fromstring(page.text)
			date = tree.xpath('//tr[@class="blu-ray"]/td[@class="value"]/text()')
			if date:
				try:
					#if the movie is already released, it will say Yes
					if date[0] == "Yes":
						movie.released = True
						print 'Released -', movie.name
					else:
						#convert string to datetime object to a date object
						movie.release = datetime.strptime(date[0], '%B %d, %Y').date()
						print movie.release, movie.name
					movie.save()
				except:
					print "No exact date -", movie.name
			else:
				print "No date -", movie.name
			time.sleep(10)
		return
