import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)

# You got wrong answer(s) for question 6,9
@app.route('/railway-builder', methods=['POST'])
def testing():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    
    # my code starts here
    result = []
    
    for entry in data:
        values = entry.split(", ")
        logging.info("values sent for evaluation {}".format(values))
        length_of_railway = int(values[0])
        number_of_types_of_track_piece = int(values[1]) # this is actually useless
        track_pieces = list(map(int, values[2:2+number_of_types_of_track_piece]))
        
        combinations = [0] * (length_of_railway + 1)
        combinations[0] = 1 # initial condition
        
        for piece in track_pieces:
            for i in range(piece, length_of_railway + 1):
                combinations[i] += combinations[i - piece]
        
        result.append(combinations[-1])
    # my code ends here

    logging.info("My result :{}".format(result))
    return json.dumps(result)
