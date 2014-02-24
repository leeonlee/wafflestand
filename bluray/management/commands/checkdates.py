from django.core.management.base import BaseCommand, CommandError
from bluray.models import Movie
from collections import defaultdict
from email.mime.text import MIMEText
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

		#Should either store release_today and send emails later or start sending out emails immediately
		email_list = defaultdict(list)
		for movie in release_today:
			for user in movie.tracking.all():
				email_list[user.email].append(movie.name)

		users = email_list.keys()
		for user in users:
			sendEmail(user)

def sendEmail(user):
	posters_formatted = ["<img src=" + '"' + movie_poster + '"' + ">" for movie_poster in email_list[user]]
	sender = "thewafflestand@gmail.com"
	pwd = "wafflestand1"
	receiver = user
	msg = MIMEMultipart('alternative')
	msg['Subject'] = 'Waffle Stand Movie Announcements'
	msg['From'] = sender
	msg['To'] = receiver
	text = "Aloha {username}! The movies you are following have been released! ".format(username = user.username) + ', '.join(email_list[user])
	html = """
		<html>
			<head></head>
			<body>
				<p>Aloha {username}!</p>
				<p>The movies you are following have been released!</p>
				{movie_posters}
				<img src="http://interfacelift.com/wallpaper/previews/03454_bonjourleman@2x.jpg">
			</body>
		</html>
	""".format(username = user.username, movie_posters = posters_formatted)
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