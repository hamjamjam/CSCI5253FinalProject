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


print("Connecting to rabbitmq({})".format(rabbitMQHost))

# Initialize the Flask application
app = Flask(__name__)

@app.route('/scan/ingredients/<X>', methods=['GET'])
def match(X):
    myingredients = X
    ingredientsList = myingredients.split(',')
    recipeURLs = ['a','b']
    return jsonify(recipeURLList = recipeURLs)


@app.route('/scan/url', methods=['POST'])
def scanUrl():
    data = request.json
    url = data["url"]
    print(url)
    
    #check if URl in db already
    #if URL already in db,
    #return jsonify(response = "recipe already in DB")
    
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
        #check if recipe exists in SQL db
        #if it does return good response
        #if bad 
        #return Response(status=500)
        return jsonify(response = "added recipe to DB")
    return jsonify(response = "request timeout")

print('pooooo')

app.debug = True
app.run(host="0.0.0.0", port=5000)


