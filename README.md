# Flappy Bird Analytical Dashboard

This program allows a user to view scores on an online analytical dashboard from the game, Flappy Bird.
You can view your own statistics of the game, and  top scores of all time.
You must sign up to play the game. No personal information needed, just username and a password.
The password is hashed with salt.

Click [here](https://fbird-analytical-dashboard.herokuapp.com/login) to login and [here](https://fbird-analytical-dashboard.herokuapp.com/signup) to sign up. 

Click [here](https://github.com/jasongalicia/Flappy-Bird-Game-Java) to view Flappy Bird Game created in Java.

## Tools/Technologies Learned/Utilized

Languages:
- HTML5
- CSS3
- Python
- MySQL

Framework:
- Flask

Version Control
- Git

Deployment:
- Heroku

Text Editors/IDE:
- Atom
- MySQL Workbench
- Sublime Text 3

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install -r requirements.txt
```

Under the "app.config" section in 'launcher.py, enter your own database information if you want to use this for your own doing.

```bash
app.config['MYSQL_DATABASE_USER'] = '(ENTER INFORMATION HERE)'
app.config['MYSQL_DATABASE_PASSWORD'] = '(ENTER INFORMATION HERE)'
app.config['MYSQL_DATABASE_HOST'] = '(ENTER INFORMATION HERE)'
app.config['MYSQL_DATABASE_DB'] = '(ENTER INFORMATION HERE)'
app.config['MYSQL_DATABASE_CURSORCLASS'] ='DictCursor'
app.config['SECRET_KEY'] = '(ENTER INFORMATION HERE)'
```

# Current Bugs Or Issues
(February 19, 2020): None at the current moment.

## Authors
- Jason Galicia

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
