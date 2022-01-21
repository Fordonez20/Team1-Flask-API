#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
import os
import boto3

from flask import Flask, jsonify, request

app = Flask(__name__)
client = boto3.client('dynamodb', region_name='us-east-1')
dynamoTableName = 'Type-Attack-LeaderBoard'


@app.route("/")
def hello():
    return "Hello World I am the Flask API! Use a Specific Route!"


@app.route("/getRecord<string:name><string:wpm><string:accuracy>")
def get_artist(name,wpm,accuracy):
    resp = client.get_item(
        TableName=dynamoTableName,
        Key={
            'name': { 'S': name },
            'wpm': { 'S': wpm },
            'accuracy': { 'S': accuracy }
        }
    )
    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'This person does not exist'}), 404

    return jsonify({
        'name': item.get('name').get('S'),
        'wpm': item.get('wpm').get('S'),
        'accuracy': item.get('accuracy').get('S')
    })


@app.route("/sendRecord", methods=["POST"])
def send_record():
    name = request.json.get('name')
    wpm = request.json.get('wpm')
    accuracy = request.json.get('accuracy')
    if not name or not wpm or not accuracy:
        return jsonify({'error': 'Please provide Name, WPM and Accuracy'}), 400

    resp = client.put_item(
        TableName=dynamoTableName,
        Item={
            'Name': {'S': name },
            'WPM': {'S': wpm },
            'Accuracy': {'S': accuracy }
        }
    )

    return jsonify({
        'Name': name,
        'WPM': wpm,
        'Accuracy': accuracy 
    })


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=5000)