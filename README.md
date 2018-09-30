# BackEnd:
## installation:
* install docker and docker_compose
* `docker-compose build`
## run the project:
*  `docker-compose up`
## access:
* `http://localhost:9080/crawl.json?url={{URL_TO_SCRAP}}&spider_name=analyzer`


# FrontEnd
## installation:
* install node and npm
* `npm install --global gulp-cli gulp`
* `cd front_end`
* `npm install`
*  `bower install`
## run the project:
* `gulp serve` to run the development server
## access:
* `http://localhost:9000/`


# stack
* scrapy (python web-crawling framework)
* scrapyrt (HTTP server which provides API for scheduling Scrapy spiders and making requests with spiders)
* splash (Lightweight, scriptable browser as a service with an HTTP API)
* varnish (caching HTTP reverse proxy)


# decisions and assumbtions
### why scrapy:
Scrapy handles so many stuff that I'd have to implement by myself if I was using something like an HTTP lib (requests) + parsing lib (buatiful soup) combination.
* Scrapy let's you crawl websites concurrently without having to deal with threads, processes, synchronization or anything else. It handles your requests asynchronously and it is really fast.
* Auto-throttling
* respects robots.txt by default
* automatically preserve sessions and handles authontication

### why splash:
many web sites builds its dom using JavaScript, so fetching fetching from the server will not be very useful, splash is a lightweight browser that can render the complete dom object by calling an http api

### varnish
using varnish as a reverse proxy enables our backend to be compact and focus on business logic, also letting the web server to serve from cash is faster and reduce the load on the backend

# TODO:
* use multi stage docker file to build the Front End
* fix Varnish setup
* let the fascade api schedules scrapping requests in **asynchronous** manner (pushing tasks in message queue) and notify the FrontEnd when it is done

# known bugs:
* response with status 200 even if the original scrapped page responds with error
* errors are not shown in the FE