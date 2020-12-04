#!/usr/bin/env python3
# 
#
# A sample REST client for the face match application
#
import requests
import json
import time
import sys, os
import jsonpickle

def doIngredients(addr, ingredients, debug=False):
    # prepare headers for http request
    headers = {'content-type': 'application/json'}
    # send http request with ingredients and receive response
    #ingredients should be string of form 'lemon,beef,rosemary'
    ing_url = addr + '/scan/ingredients'
    data = jsonpickle.encode({ "ings" : ingredients})
    response = requests.post(ing_url, data=data, headers=headers)
    if debug:
        # decode response
        print("Response is", response)
        print(json.loads(response.text))

def doUrl(addr, filename, debug=False):
    # prepare headers for http request
    headers = {'content-type': 'application/json'}
    # send http request with image and receive response
    image_url = addr + '/scan/url'
    data = jsonpickle.encode({ "url" : filename})
    response = requests.post(image_url, data=data, headers=headers)
    if debug:
        # decode response
        print("Response is", response)
        print(json.loads(response.text))

host = sys.argv[1]
cmd = sys.argv[2]

addr = 'http://{}'.format(host)

if cmd == 'ingredients':
    ingredients = sys.argv[3]
    reps = int(sys.argv[4])
    start = time.perf_counter()
    for x in range(reps):
        doIngredients(addr, ingredients, True)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
elif cmd == 'url':
    url = sys.argv[3]
    reps = int(sys.argv[4])
    start = time.perf_counter()
    for x in range(reps):
        doUrl(addr, url, True)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
else:
    print("Unknown option", cmd)
