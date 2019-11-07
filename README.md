# capstone-api

# Hello! Welcome to Size Your Drive

This Application is designed for individuals or entities
organizing a clothing drive. This application logs what items you are
planning on donating and sends an email with a PDF attachment of
your donation items to whomever is organizing the clothing drive. This
application helps the organization receiving the donations save time
sorting through the clothing by getting an itemized donation box pdf.
Furthermore, it also holds the people donating accountable by not
allowing them to donate unusable items. In addition, Some charities
are needing specific clothing so this will allow the organizer to know
where they need to send the clothing.



Please Clone down the repo

```git@github.com:westmary48/capstone-api.git```


After you clone the repo, cd into it and perform the following steps:
1. Run this command: ```python -m venv capstoneEnv```
2. Next, cd into the capstoneEnv directory within the project directory
3. Then cd into the Scripts directory and run the command: ```source ./capstoneEnv/bin/activate```
4. In the root directory run the command: ```pip install django autopep8 pylint djangorestframework django-cors-headers pylint-django```
5. Run: ```pip freeze -r requirements.txt```


The next steps are for setting up the database:
1. In the root project directory run the command: ```python manage.py makemigrations```
2. Next run: ```python manage.py migrate```
3. Then run: ```python manage.py loaddata <fixture file name minus .json>```
load order should be:
users
donator
dropoff
itemcategory
item
donationbox
itemdonationboxes


Now that your database is set up all you have to do is run the command:

```python manage.py runserver```


You can test your new server out in postman if you so desire.


Client repo:

```git@github.com:westmary48/capstone-api.git```
