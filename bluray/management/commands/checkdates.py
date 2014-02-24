from django.core.management.base import BaseCommand, CommandError
from bluray.models import Movie
from collections import defaultdict
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import datetime

'''
Checks the release dates of every movie in the database by subtracting future release date from today
Should probably check only movies that have not been released
Maybe have a boolean field or a separate model for released movies?
'''
class Command(BaseCommand):
	help = ''

	def handle(self, *args, **options):
		movies = Movie.objects.filter(released=False)
		release_today = []
		today = datetime.date.today()
		for movie in movies:
			print 'Checking', movie.name
			if movie.release != None:
				if movie.release - today <= datetime.timedelta(0):
					print movie.name, 'releasing'
					release_today.append(movie)
					movie.released = True
					movie.save()

		if release_today:
			# email_list: key = email, value = movies
			email_list = defaultdict(list)
			usernames = {}
			for movie in release_today:
				for user in movie.tracking.all():
					email_list[user.email].append(movie.name)
					# this is redundant (quick fix)
					usernames[user.email] = user.username

			users = email_list.keys()
			for user in users:
				sendEmail(user, email_list, usernames[user])

# refactor dis
def sendEmail(user, email_list, username):
	# fetch poster links corresponding to movie title - should probably be by rt-id
	posters = map(lambda movie_name: Movie.objects.get(name = movie_name).poster, email_list[user])
	posters_formatted = ' '.join(["<img src=" + '"' + movie_poster + '"' + ">" for movie_poster in posters])

	sender = "thewafflestand@gmail.com"
	pwd = "wafflestand1"
	receiver = user
	msg = MIMEMultipart('alternative')
	msg['Subject'] = 'Waffle Stand Movie Announcements'
	msg['From'] = sender
	msg['To'] = receiver
	text = "Aloha {name}! The movies you are following have been released! ".format(name = username + ', '.join(email_list[user]))
	html = """
		<html>
			<head></head>
			<body>
				<p>Aloha {name}!</p>
				<p>The movies you are following have been released!</p>
				{movie_posters}
			</body>
		</html>
	""".format(name = username , movie_posters = posters_formatted)
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')
	msg.attach(part1)
	msg.attach(part2)
	try:
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.login(sender, pwd)
		server.sendmail(sender, receiver, msg.as_string())
		server.quit()
	except Exception as e:
		print "Error: " + str(e)
