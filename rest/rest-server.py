##
from flask import Flask, request, Response, jsonify
import time
import json, jsonpickle, pickle
import platform
import io, os, sys
import pika, redis
import hashlib, requests
from PIL import Image
import base64

##
## Configure test vs. production
##
rabbitMQHost = os.getenv("RABBITMQ_HOST") or "rabbitmq"
redisHost = os.getenv("REDIS_HOST") or "redis"

print("Connecting to rabbitmq({})".format(rabbitMQHost))

redisUrltoIngredientSet = redis.Redis(host=redisHost, db=1) # Key -> Set

# Initialize the Flask application
app = Flask(__name__)

@app.route('/scan/ingredients/<X>', methods=['GET'])
def match(X):
    myingredients = X
    ingredientsSet = set(myingredients.split(','))
    #make sql req
    outputURLs = []
    for key in redisHashToFaceRec.keys():
        ingredientslist = list(redisUrltoIngredientSet.smembers(key))
        ingredients = set([ingredient.decode("utf-8") for ingredient in ingredientslist])
        if ingredients.issubset(myingredientsSet):
            outputUrls.append(key.decode("utf-8"))
     if outputURLs = []:
        outputURLs.append('No matching recipes')
     return jsonify(recipeURLList = outputURLs)


@app.route('/scan/url', methods=['POST'])
def scanUrl():
    data = request.json
    url = data["url"]
    print(url)
    
    if redisUrltoIngredientSet.exists(url):
        return jsonify(response = "recipe already in DB")
    
    message = url
    credentials=pika.PlainCredentials('guest','guest')
    parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='work')
    channel.basic_publish(exchange ='',routing_key='work', body = message)
    print(" [x] Sent Data " + url)
    connection.close()
    
    for i in range(0,10):
        time.sleep(0.75)
        if redisUrltoIngredientSet.exists(url):
            return jsonify(response = "added recipe to DB")
    return jsonify(response = "request timeout")

print('pooooo')

app.debug = True
app.run(host="0.0.0.0", port=5000)


