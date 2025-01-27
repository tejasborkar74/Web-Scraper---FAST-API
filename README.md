Web Scraper Application using FAST API

Starting Guid

1. How to run the server locally (We have 2 options): 
    OPTION 1: 
    1. run command : `uvicorn main:app --host 0.0.0.0 --port 8000`
    2. To start the application using above command you have to install all the dependencies locally
    
    OPTION 2 (Using DOCKER):
    1. This application is Dockarised, so you can just create an image and run a container of the image
    2. Create Image command: `docker build -t <IMAGE-NAME> .`
    3. Run a container using the above created image: `docker run -p 8000:8000 <IMAGE_NAME>`

2. Caching Server:
     -> If you are running server without docker then run a redis server on port mentioned in config.json
     -> If you are using docker to run server the replace the redis credentials in config.json to your own redis server and create image again.
NOTE: Even if you don't use redis it will not stop the application because it has fall back mechanism for redis


Endpoints:
1. GET `/` => Welcome page
2. POST `/auth` => to generate jwt token
3. POST `/page/{page_no}` => get data of a perticular page
4. POST `/pages` => get data of multiple page example `/pages?end_page=2&start_page=1`
5. GET `/get_data ` => get database data (data from .json file in our case)

Features:
1. Authentication
2. Single and multple page Scraping
3. Chaching - Fall back machanism of chaching server is down
4. Retry Machanism
5. Notification System (Observer Design Pattern)
6. Moduler and Easy to scale Applicaiton

