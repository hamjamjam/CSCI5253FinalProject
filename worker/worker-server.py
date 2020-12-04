#
# Worker server
#
import pika
import io
import os
import sys
import platform
import redis
import inspect
import urllib.request
from recipe_scrapers import scrape_me
from groceries import Ingredient

hostname = platform.node()

redisHost = os.getenv("REDIS_HOST") or "redis"
rabbitMQHost = os.getenv("RABBITMQ_HOST") or "rabbitmq"

print("Connecting to rabbitmq({}) and redis({})".format(rabbitMQHost,redisHost))

redisUrltoIngredientSet = redis.Redis(host=redisHost, db=1) # Key -> Set
print("initiliazed redis db")

def addRecipe(ch, method, properties, inputbody):
    try:
        body = inputbody.decode("utf-8")
        print(body)
        print('callback made')
    except Exception as e:
        print(e)
        print('error processing body')
    
    try:
        scraper = scrape_me(body)
        print('scrape successful')
    except Exception as e:
        print(e)
        print('error scraping')

    special = {'diced', 'chopped', 'squeezed', 'tablespoon', 'teaspoon', 'tbsp', 'tsp', 'tablespoons', 'teaspoons'}
    
    try:
        ings = scraper.ingredients()
        print('got ingredients (and amounts)')
    except Exception as e:
        print(e)
        print('problem with ings = scraper.ingredients()')
        
    finalings = []
    
    try:
        for ing in ings:
            parseding = Ingredient(ing)
            finaling = parseding.name
            if finaling.split(' ')[0] in special:
                finaling = " ".join(finaling.split(' ')[1:])

        finalings.append(finaling)

        redisUrltoIngredientSet.sadd(body, *ingredients)
        
    except Exception as e:
        print(e)
        print('error parsing and then writing to redis')
          
          
def main():
    print('running main')
    
    credentials=pika.PlainCredentials('guest','guest')
    parameters = pika.ConnectionParameters(rabbitMQHost, 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    #connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitMQHost))
    channel = connection.channel()
    channel.queue_declare(queue='work')
    print('connection made')
    print(inspect.getargspec(channel.basic_consume))

    channel.basic_consume(queue='work', on_message_callback=addRecipe, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
