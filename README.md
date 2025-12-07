### INF601 - Advanced Programming in Python
### Iris Perry
### Final Project
 
 
# GameShelf
 
A web application that allows users to search video games, organize them into a personal game library, and leave ratings and reviews for games.
 
## Description
 
GameShelf is a Django-based web application that lets users search for video games using the RAWG Video Games Database API. Users can create accounts, log in, save games to a personal library, track their play status as Want to Play, Currently Playing, or Played. Users can also leave ratings and written reviews for games. The goal of this project is to give gamers a centralized place to track their gaming backlog across multiple platforms.
 
## Getting Started
 
### Dependencies
 
* Python 3.11+
* Django 5.2.8
* Requests
* Pillow (for image uploads)
* An active RAWG API key
* Supported OS: Windows 11

Install required packages:
```
pip install -r requirements.txt
```
 
### Installing
 
* Clone or download the project:
```
git clone https://github.com/zeldafreak489/finalprojectIrisPerry
cd game_shelf
```
* Create a .env fils in the project root and add:
```
RAWG_API_KEY=your_api_key_here
```
* Apply database migrations:
```
python manage.py migrate
```
* Create a superuser (optional, for admin access):
```
python manage.py createsuperuser
```
 
### Executing program
 
To run the development server:
```
python manage.py runserver
```
Steps to use:
* Open a browser and go to http://127.0.0.1:8000
* Create an account or log in
* Use the search bar to find games
* Add games to your personal library
* Leave ratings and reviews on games
 
## Help

If the server won't start, try:
```
python manage.py makemigrations
python manage.py migrate
```
If static files or images are not displaying, check that:
* MEDIA_URL and MEDIA_ROOT are correctly set in settings.py
* Your .env file is loading correctly
 
## Authors

Iris Perry 
[LinkedIn](https://www.linkedin.com/in/iris-perry-5933b5137/)
 
## Version History
 
* 0.2
    * Added ratings and review system
    * User profiles with profile pictures
    * Library status tracking
* 0.1
    * Initial Release
 
## Acknowledgments
 
* [RAWG Video Games Database API](https://rawg.io/apidocs)
* [Django Documentation](https://docs.djangoproject.com/en/5.2/)
* [Bootstrap 5](https://getbootstrap.com/docs/5.3/getting-started/introduction/)