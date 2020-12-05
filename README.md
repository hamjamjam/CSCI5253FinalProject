# CSCI 5253 Final Project
Jamie Voros
Collaborators: None
Fall 2020

# Work process

## Create a kubernetes cluster

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

## Use existing setup from lab7 to create server API pod, expose to public
Use what we already have from lab 7 to deploy a REST API server/client pair. Make sure it's set up as load balancer.

### Debug
Thankfully these guys were already set up from lab 7 to write to logs (server) or display error messages when called (client).

## Use existing setup from lab7 to create a client API that can send either 'recipe to add' or 'ingredients to match'
Recipe to add will send the url to rabbitMQ.
Ingredients to match will query the Recipes table.
