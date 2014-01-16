'''
Define the tasks to be done by async workers
'''

from bluray.models import *
import datetime
import mechanize
from lxml import html
import time
'''
Checks the release dates of every movie in the database by subtracting future release date from today
Should probably check only movies that have not been released
Maybe have a boolean field or a separate model for released movies?
'''
def check_dates():
	movies = Movie.objects.all()
	release_today = []
	for movie in Movies:
		if movie.release - datetime.date.today() == datetime.timedelta(0):
			release_today.append(movie)

	'''
	Should either store release_today and send emails later or start sending out emails immediately
	'''

'''
Scrape the dates of all movies in the database
Probably want to not scrape for movies already with dates
'''
def scrape_dates():
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

		time.sleep(1)
		tree = html.fromstring(br.response().read())
		try:
			date = tree.xpath('//span[@style="color: #666666"]/a[@style="text-decoration: none; color: #666666"]/text()')[0]
			movie.release = datetime.datetime.strptime(date, '%b %d, %Y').date() #convert string to datetime object to a date object
			movie.save()
		except: #if exception occurs, then there is no release date
			pass

		time.sleep(30)
	return

'''
Method to generate new movie objects
Probably should scrape new releases
or maybe http://www.rottentomatoes.com/movie/box-office/
if they're out in theaters still then they probably dont have blu ray out
run once a week?
'''
def scrape_movies():
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

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
