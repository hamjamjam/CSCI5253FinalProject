# CSCI 5253 Final Project

To do:

## Create a kubernetes cluster

## Use existing RabbitMQ setup from lab7 to create queue pod
I don't anticipate changing much

## Use existing setup from lab7 to create worker pod that listens to queue, scrapes and writes to database
Need to install scraper https://github.com/hhursev/recipe-scrapers

## Use existing setup from lab7 to create worker pod that implements bogosort as a service (writes to Redis DB?)
Takes in list to be sorted. Once done, it adds list and sorted version to Redis db. Once found, it removes list and sorted version from redis db and returns to client.
(would require whipping up redis db as well)

## Create MySQL database using GCP (TBD if it's within Kube)
??? haven't really done this before. Will contain just one table:

RECIPES
URL | ingredient_id | number_ingredients

Using this, I will be able to filter on 'ingredient_id' in set (of ingredients) and then filter again on count (grouped by URL); if the count matches number_ingredients then that recipe contains ingredients that the user has.

``SELECT URL, count(*) as cnt, number_ingredients from RECIPE where
Ingredient_id in {USERINPUT_SET} AND cnt == number_ingredients
Group by URL, number_ingredeitns
``

## Use existing setup from lab7 to create server API pod, expose to public
Use what we already have from lab 7 to deploy a REST API server/client pair. Make sure it's set up as load balancer.

## Use existing setup from lab7 to create a client API that can send either 'recipe to add' or 'ingredients to match'
Recipe to add will send the url to rabbitMQ.
Ingredients to match will query the Recipes table.
