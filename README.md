# MusicForTheFam
Making latest music uploads reach to the members of Fampay. I call it FamTube!

# Tech Stack Used
Backend: Django Rest Framework, Django, Redis, Celery
<br />
Frontend: Vue.js
<br />
Database: PostGresSQL
<br />
DevOps: AWS, Gunicorn, NGINX
<br />
Search Query Used: Official Music

# Endpoints
1) GET API (get all stored videos in the database sorted in reverse chronological order by publishedAt)
GET http://localhost:8000/get_all_videos?page=1 (localhost)
<IP>

2) SEARCH API (search for title and description containing search keywords)
POST http://localhost:8000/search (Headers:"Content-Type":"application/json", body:{'search':'query'}) (localhost)
<IP>
  
3)ASYNC YOUTUBE API (hits every 60 seconds to fetch latest videos)
Not a REST API, but achieved through Redis, Celery Beat and Celery Worker. Explained below :) 
  
# Methodology 
I have used Django Rest Framework to server RESTful APIs which are then consumed by Vue.js Frontend. The database is hosted externally over AWS EC2 instance and is connected with the Django backend using psycopg2. The Async Youtube API has been designed using Redis as Broker and Celery as a worker. The Celery beat schedules a get_youtube_videos task every 60seconds which is recieved and executed by the Celery Worker and the data keeps on getting fetched and the database keeps on updating till the max_interval reaches or youtube daily quota expires. Whereas the GET API and SEARCH API are server using DRF Views.

Taking this to a level forward have hosted the backend at an t2.micro EC2 instance (free tier eligible), supervised by Gunicorn which keeps the backend server running and alive. The PostGresSQL server is hosted over here too. NGINX has been configured to handle reverse proxies. The celery beat and celery worker could have been supervised too but then the daily quota would expire before you could even test it, so I didn't.

# Steps to test GET and SEARCH API:
1) Clone the repository
2) cd backend
3) Activate Virtual Enviroment - pipenv shell
4) Install Required Dependencies - pipenv install
5) cd core
6) python manage.py runserver
7) This makes the Django server up and running which lets you test the GET API and SEARCH API

# Steps to test Async Youtube API :
1) Clone the repository (ignore if already done)
2) cd backend
3) Activate Virtual Enviroment - pipenv shell
4) Install Required Dependencies - pipenv install (ignore if already done)
5) cd core
6) Install Redis into your machine
7) Run the Redis Server by running the commad "redis-server" at port 6379
8) Make sure the Redis Server is up by hitting it with a ping and if it's up you'll get a PONG back.  
9) celery -A core worker -P gevent (for windows)
10) celery -A core worker (should work for Mac, have only tested for Windows. The change because Windows doesn't support Celery 4.x and above)
11) celery -A core beat -l info --max-interval <time_in_seconds_for_which_you_want_to_keep_hitting_every_1_minute>
