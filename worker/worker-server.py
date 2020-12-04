#
# Worker server
#
import pika
import io
import os
import sys
import platform
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
  
    scraper = scrape_me(inputbody)

    special = {'diced', 'chopped', 'squeezed', 'tablespoon', 'teaspoon', 'tbsp', 'tsp', 'tablespoons', 'teaspoons'}

    ings = scraper.ingredients()
    finalings = []
    
    for ing in ings:
        parseding = Ingredient(ing)
        finaling = parseding.name
        if finaling.name.split(' ')[0] in special:
            finaling = " ".join(finaling.name.split(' ')[1:])
            
    finalings.append(finaling)
    
    redisUrltoIngredientSet.sadd(url, *ingredients)
          
          
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
