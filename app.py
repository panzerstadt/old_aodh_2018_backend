#!/usr/bin/env python
# -*- coding: utf-8 -*-

# flask stuff
from flask import Flask, request, jsonify
from flask_cors import CORS

# ml stuff


# pretty interface
from flasgger import Swagger

# CORS for connecting with the front
allowed_domains = [
    r'http://localhost:5000',
]

application = Flask(__name__)
swagger = Swagger(application)

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
@application.route('/v1/predict/', methods=['GET'])
def nn_prediction():
    """
    predicts iris type from GET
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
    x_1 = request.args.get("s_length")
    x_2 = request.args.get("s_width")
    x_3 = request.args.get("p_length")
    x_4 = request.args.get("p_width")

    x_input = [x_1, x_2, x_3, x_4]
    print('4 inputs received: ', x_input)

    #results = predict_iris(x_input=x_input)
    results = x_input

    output = {
        "results": results,
        "status": 200
    }
    return jsonify(output)


# POST request (file input)
@application.route('/v1/predict/', methods=['POST'])
def nn_prediction_file():
    """
    use case: normal user who just has a csv, and doesn't know data science. input csv, get result (datawrapper). supports multiple inputs. each input in the file must be a row of 4 numbers separated by corners in this order: sepal_length, sepal_width, petal_length, and petal_width
    ---
    parameters:
      - name: input_file
        in: formData
        type: file
        required: true
    responses:
      200:
        description: Json describing classes for each row in csv
        schema:
          id: predictionFile
          properties:
            results:
              type: json
              default: ['setosa', 'setosa', 'virginica']
            status:
              type: number
              default: 200
    """
    x_1 = request.files.get("input_file")

    #results = predict_iris_file(x_file_input=x_1)
    results = x_1
    print('returning: ', results)

    output = {
        "results": results,
        "status": 200
    }
    return jsonify(output)


application.run(debug=True)
print('a flask app is initiated at {0}'.format(application.instance_path))
