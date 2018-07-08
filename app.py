#!/usr/bin/env python
# -*- coding: utf-8 -*-

# flask stuff
from flask import Flask, request, jsonify
from flask_cors import CORS

# component
from make_tweet_list import get_tweet_list

# pretty interface
from flasgger import Swagger

# CORS for connecting with the front
allowed_domains = [
    r'http://localhost:5000',
]

application = Flask(__name__)
Swagger(application)

CORS(application,
     origins=allowed_domains,
     resources=r'/v1/*',
     supports_credentials=True)
# only allows access to listed domains (CORS will only be applied to allowed_domains
# only allows access to v1 (CORS will only be applied to domains that start with /v1/*
# IMPORTANT: supports_credentials is allows COOKIES and CREDENTIALS to be submitted across domains


# more CORS settings here: https://flask-cors.corydolphin.com/en/latest/api.html#extension
# github example: https://github.com/corydolphin/flask-cors/blob/master/examples/app_based_example.py


# only POST
@application.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        print(request)
        a = request.args.get('a')
    if request.method == 'POST':
        print(request)
        a = request.form['a']
    else:
        return "the purpose of this app is to allow the user to see the bigger picture" \
               " in the event of disasters, and not be scared by a few social media posts" \
               " that exaggerate the problem"


    return "hello {}".format(a)


# GET request
@application.route('/v1/list/', methods=['GET'])
def nn_prediction():
    """
    get list of latest tweets, locations, sentiment, and time
    ---
    parameters:
      - name: s_length
        in: query
        type: number
        required: true
      - name: s_width
        in: query
        type: number
        required: true
      - name: p_length
        in: query
        type: number
        required: true
      - name: p_width
        in: query
        type: number
        required: true
    responses:
      200:
        description: All is well. you get your results as a json with a string describing classes
        schema:
          id: predictionGet
          properties:
            results:
              type: json
              default: setosa
            status:
              type: number
              default: 200
    """
    response = get_tweet_list()

    output = {
        "results": response,
        "status": 200
    }
    return jsonify(output)



application.run(debug=True)
print('a flask app is initiated at {0}'.format(application.instance_path))
