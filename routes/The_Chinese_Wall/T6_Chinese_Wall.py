import json
import logging

from flask import request, Response

from routes import app

# My import


logger = logging.getLogger(__name__)

@app.route('/chinese-wall', methods=['POST'])
def add_oil():
    lesson_requests = request.get_json()
    
    # logging.info("data sent for evaluation {}".format(lesson_requests))

    response_data = json.dumps({
    "1": "Fluffy",
    "2": "Galactic",
    "3": "UBS",
    "4": "UBS",
    "5": "UBS"
})

    return Response(response_data, mimetype='application/json')
