from flask import Flask, render_template, url_for, request, redirect, session
from flaskext.mysql import MySQL
from crypto import Encrypt
from date import Date
from datetime import timedelta
from analysis import Analysis, Sorter
import os

# Create the Flask application and other configurations
mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_HOST'] = ''
app.config['MYSQL_DATABASE_DB'] = ''
app.config['MYSQL_DATABASE_CURSORCLASS'] ='DictCursor'
app.config['SECRET_KEY'] = 'sdfgdsf3e45t64egr45guf@224532$#^dfg64'

mysql.init_app(app)

con = mysql.connect()
cursor = con.cursor()

# Create these two tables at the start, just in case tables get deleted from
# the database.
cursor.execute('''CREATE TABLE IF NOT EXISTS admin_credentials
(id int NOT NULL AUTO_INCREMENT, username varchar(50) NOT NULL,
password varchar(255), date_created DATE, PRIMARY KEY(id))''')
cursor.execute('''CREATE TABLE IF NOT EXISTS flappy_scores
(id int NOT NULL AUTO_INCREMENT, username varchar(50) NOT NULL,
score int, date_scored DATE, PRIMARY KEY(id))''')

# When the website loads, it will automatically be redirected to the login page
@app.route("/")
def index():
	# See if the user is in session
	if "user" in session:
		return redirect(url_for('home'))
	else:
		return redirect(url_for('login'))

# The route and the method for loging in, which uses both GET, and POST
@app.route("/login", methods=['GET', 'POST'])
def login():
	# If there is a user in session
	if "user" in session:
		return redirect(url_for('home'))
	else:
		# Post method
		if request.method == 'POST':

			# Establish the connection
			cursor = mysql.get_db().cursor()

			# Grab the information from the form
			username_input = request.form['username']
			password_input = request.form['password']

			# Execute the query
			cursor.execute('''SELECT * FROM admin_credentials WHERE
				username=%s''', username_input)

			# Row count equalling zero means that no username exists
			# in the database
			if cursor.rowcount == 0:
				print('The username entered does not match'
				 + 'any record in our database')
				return render_template('login.html',
				title="Scores Login | Flappy Scores", fail_login=True)
			else:
				results = cursor.fetchone()

				# This is the actual password associated with the username in
				# encrypted form
				encrypted_real_password = results[2]

				# Hash the password
				crypt = Encrypt(password_input)
				# Get the length of the input for the password
				length_input = len(password_input)
				# New word variable needed for this process
				word = ''
				# For loop runs through until length_input
				for i in range(0, length_input):
					word = crypt.get_hashed_saltspot(i)
					if word == encrypted_real_password:
						session["user"] = username_input
						return redirect(url_for('home'))
				# Will return a failed login screen if the password is wrong
				return render_template('login.html',
				title="Scores Login | Flappy Scores", fail_login=True)
		# If its a GET, if loading up the website for the first time
		else:
			return render_template('login.html',
				title="Scores Login | Flappy Scores", fail_login=False)

# If the user wants to sign up
@app.route("/signup", methods=['GET', 'POST'])
def signup():
	if "user" in session:
		return redirect(url_for('home'))
	else:
		# Post
		if request.method == 'POST':
			# All the information from the form
			username_input = request.form['username']
			username_confirm = request.form['confirm-username']
			password_input = request.form['password']
			password_confirm = request.form['confirm-password']

			# If the usernames match
			if username_input == username_confirm:
				# If the passwords match
				if password_input == password_confirm:
					# Connect to the databse and execute a query
					con = mysql.connect()
					cursor = con.cursor()
					cursor.execute('''SELECT * FROM admin_credentials
					WHERE username=%s''', username_input)
					# This means that no username exists
					if cursor.rowcount == 0:
						date = Date()
						date_today = date.todays_date()
						crypto = Encrypt(password_input)
						new_password = crypto.get_hashed_salt()
						cursor.execute('''INSERT INTO admin_credentials
						(username, password, date_created) VALUES (%s, %s, %s)''',
						(username_input, new_password, date_today))
						# We have to commit in order for it to be actually
						# sent to the database
						con.commit()
						return render_template('signup.html',
						title="Signup | Flappy Scores", success=True)
					else:
						# The username exists in the database
						return render_template('signup.html',
						title="Signup | Flappy Scores", user_exists=True)
				else:
					# Passwords the user entered do not match at all
					return render_template('signup.html',
					title="Signup | Flappy Scores", match_error=True)
			else:
				# Usernames the user entered do not match at all
				return render_template('signup.html',
				title="Signup | Flappy Scores", match_error=True)
		else:
			# Get
			return render_template('signup.html',
			title="Sign Up | Flappy Scores", match_error=False)

# The link to access the hope page
@app.route("/home")
def home():
	if "user" in session:
		user = session["user"]
		c = mysql.get_db().cursor()
		c.execute(''' SELECT * FROM flappy_scores''')
		# All the rows of everything scored
		results = c.fetchall()

		# Getting today's date
		date = Date()
		todays_date = date.todays_date()

		analysis = Analysis(results)

		# All Statistics needed for the home page
		today_average_score = analysis.get_avg_score(todays_date)
		monthly_average_score = analysis.get_currentmonth_avg(todays_date)
		yearly_average_score = analysis.get_yearly_avg(todays_date)
		lifetime_average_score = analysis.get_lifetime_avg()

		# Today's standard deviation and variance
		today_sd = analysis.get_sd(todays_date)
		today_v = analysis.get_v(todays_date)

		sorter = Sorter()
		todays_games_played = analysis.get_games_played(todays_date)
		todays_scores = analysis.get_scores_list(todays_date)
		new_list = tuple()

		new_list = sorter.sort_descending(todays_scores)

		highest_score = 0.0
		if len(new_list) == 0:
			highest_score == 0.0
		else:
			highest_score = float(new_list[0][2])
		all_scores_list = analysis.get_list()

		# List of all the statistics to be displayed on the home page
		statistics = [today_average_score, monthly_average_score,
			yearly_average_score, lifetime_average_score, today_sd, today_v,
				highest_score, todays_games_played]
		all_scores_length = analysis.get_list_length()
		print('Here is the list: ' + str(all_scores_list))

		return render_template('home.html', title="Home | Flappy Scores",
			stats=statistics, recent_scores=all_scores_list,
				all_scores_length=all_scores_length, username=user)
	else:
		return redirect(url_for('login'))

# The top 10 scores of all time web page
@app.route("/scorestop10")
def scores_top10():
	if "user" in session:
		user = session["user"]
		c = mysql.get_db().cursor()
		c.execute(''' SELECT * FROM flappy_scores''')

		results = list(c.fetchall())

		# To get the top 10 scorers
		sorter = Sorter()
		top_list = sorter.sort_descending(results)
		list_length = len(top_list)

		return render_template('top10.html', title="Top 10 | Flappy Scores",
			top_scores=top_list, list_length=list_length,
				username=user)
	else:
		return redirect(url_for('login'))

# The top 25 scores of all time web page
@app.route("/scorestop25")
def scores_top25():
	if "user" in session:
		user = session["user"]
		c = mysql.get_db().cursor()
		c.execute(''' SELECT * FROM flappy_scores''')

		results = list(c.fetchall())

		# To get the top 25 scorers
		sorter = Sorter()
		top_list = sorter.sort_descending(results)
		list_length = len(top_list)

		return render_template('top25.html', title="Top 25 | Flappy Scores",
			top_scores=top_list, list_length=list_length,
				username=user)
	else:
		return redirect(url_for('login'))

# The top 50 scores of all time web page
@app.route("/scorestop50")
def scores_top50():
	if "user" in session:
		user = session["user"]
		c = mysql.get_db().cursor()
		c.execute(''' SELECT * FROM flappy_scores''')

		results = list(c.fetchall())

		# To get the top 50 scorers
		sorter = Sorter()
		top_list = sorter.sort_descending(results)
		list_length = len(top_list)

		return render_template('top50.html', title="Top 50 | Flappy Scores",
			top_scores=top_list, list_length=list_length,
				username=user)
	else:
		return redirect(url_for('login'))

# The top 100 scores of all time web page
@app.route("/scorestop100")
def scores_top100():
	if "user" in session:
		user = session["user"]
		c = mysql.get_db().cursor()
		c.execute(''' SELECT * FROM flappy_scores''')

		results = list(c.fetchall())

		# To get the top 100 scorers
		sorter = Sorter()
		top_list = sorter.sort_descending(results)
		list_length = len(top_list)

		return render_template('top100.html', title="Top 100 | Flappy Scores",
			top_scores=top_list, list_length=list_length,
				username=user)
	else:
		return redirect(url_for('login'))

# Lifetime report, all statistics
@app.route("/report-lifetime")
def lifetime_report():
	if "user" in session:
		user = session["user"]
		date = Date()
		current_date = date.todays_date()

		c = mysql.get_db().cursor()
		c.execute(''' SELECT * FROM flappy_scores''')

		results = list(c.fetchall())

		sorter = Sorter()
		scores = sorter.sort_ascending(results)
		analysis = Analysis(scores)
		stats_length = len(scores)

		avg_score = analysis.get_lifetime_avg()
		median = analysis.get_lifetime_median()
		sd = analysis.get_lifetime_sd()
		variance = analysis.get_lifetime_v()
		above_median = analysis.get_above_medp()
		equal_median = analysis.get_equal_medp()
		scores = sorter.sort_descending(results)

		below_median = 100.0 - above_median - equal_median

		statistics = [avg_score, median, sd, variance, above_median, below_median,
			equal_median]

		return render_template('lifetimereport.html',
			title="Lifetime Report | Flappy Scores", top_scores=scores,
				stats_length=stats_length, statistics=statistics,
					todays_date=current_date, username=user)
	else:
		return redirect(url_for('login'))

# To access the user's profile and stats
@app.route("/profile")
def profile():
	if "user" in session:
		user = session["user"]
		date = Date()
		current_date = date.todays_date()

		c = mysql.get_db().cursor()
		c.execute(''' SELECT * FROM admin_credentials''')

		results = list(c.fetchall())
		analysis = Analysis(results)
		date_created = analysis.get_profile_datejoined(user)

		c.execute(''' SELECT * FROM flappy_scores''')
		results = list(c.fetchall())
		analysis = Analysis(results)

		best_score = analysis.get_profile_bestscore(user)
		avg_score = analysis.get_profile_avgscore(user)
		gp = analysis.get_profile_gp(user)

		recent_games = analysis.get_rec_usergames(user)
		recent_games_length = len(recent_games)

		print('This users best score is ' + str(best_score))
		print('This users average score is ' + str(avg_score))
		print('This users games played is ' + str(gp))
		print(recent_games_length)

		stats = [best_score, avg_score, gp]
		return render_template('profile.html',
			title="My Profile | Flappy Scores", username=user,
				date_created=date_created, stats=stats,
					recent_games=recent_games,
						recent_games_length=recent_games_length)
	else:
		return redirect(url_for('login'))

# Logout, so that no one can access this url. It would be very hard to
@app.route("/dslkjhdfgh456*3")
def logout():
	if "user" in session:
		session.pop("user", None)
		return redirect(url_for('login'))
	else:
		return redirect(url_for('login'))

# Handles error links
@app.errorhandler(404)
def page_not_found(e):
	return render_template('forbiddenaccess.html', title="404 Error | Flappy Scores")

# What the user sees when the server crashes for whatever reason
@app.errorhandler(500)
def server_error(e):
	return render_template('servererror.html', title="500 Server Error | Flappy Scores")

# Testing pages purposes only
#@app.route("/testpage")
#def testpage():
#	return render_template('servererror.html', title="500 Server Error | Flappy Scores")

# For test development, this is needed but when deploying to heroku, it's not needed at all.
if __name__ == '__main__':
	app.run(Debug=True)
