'''
Define the tasks to be done by async workers
'''

from bluray.models import *
from datetime import date, timedelta

'''
Checks the release dates of every movie in the database by subtracting future release date from today
Should probably check only movies that have not been released
Maybe have a boolean field or a separate model for released movies?
'''
def check_dates():
	movies = Movie.objects.all()
	release_today = []
	for movie in Movies:
		if movie.release - date.today() == timedelta(0):
			release_today.append(movie)

	'''
	Should either store release_today and send emails later or start sending out emails immediately
	'''

'''
Method to scrape the dates somehow.
'''
def scrape_dates():
	return 0
