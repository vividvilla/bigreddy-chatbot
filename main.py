# -*- coding: utf-8 -*-

import logging

from flask import Flask, request, json
from bigreddy import BigReddy

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    """Handles an event from Hangouts Chat."""
    if request.method == 'GET':
        return json.jsonify({'message': 'Hello there!'})

    event = request.get_json()
    if event['type'] == 'ADDED_TO_SPACE' and event['space']['type'] == 'ROOM':
        text = 'Thanks for adding me to "%s"!' % event['space']['displayName']
        return json.jsonify({'text': text})
    elif event['type'] == 'MESSAGE':
        ramble = BigReddy().ramble()
        text = ramble
        return json.jsonify({
                            'cards': [{
                                'sections': [{
                                    'widgets': [{
                                        'textParagraph': {
                                            'text': text
                                        }
                                    }]
                                }]
                            }]
                            })
    else:
        return


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
