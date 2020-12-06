# CSCI 5253 Final Project
Jamie Voros

Collaborators: None

Fall 2020

# Project Description
Title: Ingredients to Recipe (with ability to add to database) as a Service

### Overview and Goals
1.	Take a set of ingredients as input and return a list of recipe URLs to online recipes that can be made with the ingredients

2.	Take a recipe URL, scrape it and add the URL and ingredients set to the database

### Software and Hardware
#### Software:

Database - Redis

Queue – RabbitMQ

API – REST server and client

Listener and scraper (scraping done by https://github.com/hhursev/recipe-scrapers and https://github.com/tobiasli/groceries.git)

#### Hardware/Infrastructure:

Kubernetes Cluster (hosted via GCP)

### Diagram

![](image.png)

#### Database Schema

A single key to set store in Redis going from recipe URL to the set of its ingredients.

### Components
#### Kubernetes Cluster

Purpose: to house the project

Why: It was much faster to be able to whip up and kill pods during testing (than it would have been had I been using entire VMs). Additionally, Docker has a lot of support and existing images which made setting up every other component much easier.

Interactions: It houses all the following components


#### API

Purpose: This was the interface; this is how the user interacts with the service as a whole.

Why: I chose REST (over grcp) because, although grcp can be superior if running many queries which can use the same connection, this is unlikely to happen here. Additionally, we already had this set up on kube for lab 7, which made selecting the base Docker image and building the Dockerfile much easier.

Interaction:  The client interacts with the user. The user uses the client script to pass requests to the server.

The server takes requests from the client and either passes them to RabbitMQ (when adding a recipe to the database) or processes the request from the client and hands and output back (when returning matching recipes).


#### Database

Purpose: To store all of our recipe data.

Why: Redis is a really nice way to store key -> set stores. I had originally planned to use some kind of SQL style database, but it proved much easier to take advantage of Redis’ k,v store allowing the ‘v’ part to be a set (which SQL does not do as well).

Interaction: Redis is written into by the worker node only. Redis is queried by the REST server only.


#### Queue

Purpose: To avoid sending work to the worker node while it is still working. The queue allows the REST server to not have to confirm that the worker is ready for another request.

Why: RabbitMQ has amazing doc files. Here, we needed just one queue (although Rabbit has quite a lot of functionality).

Interactions: Rabbit is handed messages by the REST server and will pass them to worker nodes listening to the appropriate queue.


#### Worker

Purpose: Where all the hard work happens. The worker exists to do the recipe crunching and to write the appropriate information to the database.

Why: The scraping and writing was too much to happen on the REST server itself, therefore it hands off the hard work to the worker.

Interactions: The worker is listening to one of Rabbit’s queues. When it gets a message from RabbitMQ, the worker processes the recipe and writes the recipe and ingredients to the database.

### Capabilities and Limitations

#### Capabilities

The service can take in a url linking to an online recipe, scrape it and write to a database. When a url is submitted, the service will return one of three things:

•	The recipe is already in the database

•	The recipe has been added to the database

•	There was an error or timeout


The service can take a comma separated list of pantry items and will return one of two things when submitted:

•	These are the matching recipe urls

•	There are not matching recipes


#### Limitations

The service is not very robust. The scraper component is not perfect. The recipe is scraped down to its ingredients and also quantities and descriptions (e.g. “one cup lemon juice” or “1/2 chopped onion” or “1 pound lean ground pork”). Going from ingredients that contain a description (e.g. “chopped onion”) to the pantry item (e.g. “onion”) proved quite difficult.

The service also needs to drop everything to singulars, sometimes, depending on how the scraping runs, an item like “eggs” may show up as “egg” or “eggs”, which means that the user has to put both the singular and plural into their request. This could be solved by having a standardized library of ingredients and having an algorithm assign each ingredient that comes in (either via the recipe scraper or user input) to one in its standardized library. There may be some miss-assignment, but in the world of cooking and recipes, a lot of ingredients can be substituted anyway.

Further work could be done on ingredient quantities. This would require the service to be able to take each ingredient quantity and convert it to a common unit (sometimes the recipes call for cups of flour, others call for grams).

Another point of lack of robustness is that right now there is no check of whether the url is a recipe url, the service just blindly tries to scrape and will still add whatever comes back (even if empty) to the database.


# Work process

## Create a kubernetes cluster
```
gcloud config set compute/zone us-central1-b
gcloud container clusters create --preemptible mykube
```

## Use existing RabbitMQ and Redis setups from lab7 to create queue pod
I did not need to change anything here. I was able to copy the Rabbitmq and Redis folders over and deploy the two services without an issue.

### Debug
To ensure that rabbitmq was getting messages, I deleted the worker deplyoment, used the rest client to send a request, moved to the rabbit container's shell and requested queue information with `rabbitmqctl list_queues`. It shows the number of messages in the queue (I could see my message). I then started the worker, went back to the rabbit shell and ran the same command again. This time, there were no messages remaining in the queue, indicating that the worker had consumed them.

To ensure that redis was working appropriately, I was able to hit either the rest or worker shell and use python3 in the command line. I was able to verify being able to read a write to dbs in redis.

## Use existing setup from lab7 to create worker pod that listens to queue, scrapes and writes to database
Here I used the existing framework from lab 7 to create a worker server that listens to RabbitMQ's work queue.

In order to get the scraping done, I used the standard python docker image (`https://hub.docker.com/_/python`) and cloned the following two repos into it for my scraping:

```
https://github.com/hhursev/recipe-scrapers
https://github.com/tobiasli/groceries.git
```

The recipe-scrapers repo allowed me to scrape the ingredients (and their amounts) from a recipe and retain its URL. The groceries repo allowed me to scrape a list of bare items (or grocery list) from the ingredients of each recipe.

I then set up a worker-server to listen to Rabbit's work queue and to process recipe scraping as requests came in.

Once each recipe was scraped and processed into a set of ingredients, I added the recipe to a redis database.

### Debug

I set the pod to write python output to log files and wrote a script to pull up the logs. Prior to having the worker listen to the queue, I used the shell to ensure that the scraping process worked and write to the database as desired (key -> set stores).

Rabbit is pretty frustrating in that error messages aren't printed if an error occurs in its callback function. Therefore, I wrapped most of that in various try excepts in order to get at my error messages. There are numerous print statements (that print to the log file) telling me where the script 'got to'.

## Use existing setup from lab7 to create rest server and client
Use what we already have from lab 7 to deploy a REST API server/client pair. Make sure it's set up as load balancer.

The rest API can take two types of inputs - the url of a recipe to be scraped or a comma separated list of pantry items.

If a url is given, the server passes the url to rabbit (who hands it to the worker).

If a list of ingredients is given, the server searches through the redis database and returns the urls of all the recipes for which the recipe-required ingredietns are a subset of the pantry items passed in

### Debug
Thankfully these guys were already set up from lab 7 to write to logs (server) or display error messages when called (client).

## Scripts hanging out
`get-logs.sh` retuns log files for the specificed pod

`rest/build-test.sh` builds the rest server

`rest/test-client.sh` tests the url input to rest, takes url argument. If none give, uses standard

`rest/test-client-get.sh` tests the ingredient list input

`worker/Makefile.sh` builds the worker node
