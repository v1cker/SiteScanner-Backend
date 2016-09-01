## Site Scanner

<img width="400" height="182" alt="Django" src="https://www.djangoproject.com/s/img/logos/django-logo-negative.png" />
	
Django application that monitors your websites and gives you alerts if something goes wrong.

This project works as an API for app written in Ember. More details here:<br>
[https://github.com/Josowsky/SiteScannerFrontEnd](https://github.com/Josowsky/SiteScannerFrontEnd)

Aside from API there is also Django application with GUI used for management. 

## Inspiration

Idea for crawler that monitors websites came from here:<br>
[https://uptimerobot.com/](https://uptimerobot.com/)

I started with Django thanks to this tutorial:<br>
[https://www.youtube.com/playlist?list=PLEsfXFp6DpzRcd-q4vR5qAgOZUuz8041S](https://www.youtube.com/playlist?list=PLEsfXFp6DpzRcd-q4vR5qAgOZUuz8041S)

## Libraries used:

* Django REST Framework
* Django OAuth Toolkit
* Django REST Framework JSONAPI
* Django Registration Redux
* Requests
* Celery
* Beautiful Soup
* Django Crispy Forms
* Django CORS Headers

## Setup

Clone the repository.

Install requrements:
```sh
pip install -r requrements.txt
```
Migrate the database:
```sh
python manage.py makemigrations
python manage.py migrate
```

Create admin user:
```sh
python manage.py createsuperuser
```

To run the server use:
```sh
python manage.py runserver
```
By default, app will be live at http://localhost:8000

## References
* [OAuth2 with Django REST Framework](https://yeti.co/blog/oauth2-with-django-rest-framework/)
* [Django REST Frameowrk JSNO API format](https://github.com/django-json-api/django-rest-framework-json-api)
* [Asyncs task in Django with Celery and Redis](http://michal.karzynski.pl/blog/2014/05/18/setting-up-an-asynchronous-task-queue-for-django-using-celery-redis/)
* [Supervisor (manage process on the server)](http://supervisord.org/)
* [DRF documentation](http://www.django-rest-framework.org/)
* [Requests docs](http://docs.python-requests.org/en/latest/index.html)
* [Setting up JSONAPI and models with relations](http://django-rest-framework-json-api.readthedocs.io/en/v2.0.1/usage.html#setting-the-resource-name)
