import json
import logging

from flask import request

from routes import app

# My import

logger = logging.getLogger(__name__)

@app.route('/greedymonkey', methods=['POST'])
def testing():
    data = request.get_json()
    # logging.info("data sent for evaluation {}".format(data))
    
    # my code starts here
    result = 0

    n = len(data["f"]) # the number of fruit
    max_w = data["w"] # the maximum weight of fruit
    max_v = data["v"] # the maximum volume of fruit

    # try try top down dp
    dp = [[0 for _ in range(max_v+1)]  for __ in range(max_w+1)] # dp[i][j] is the max val for weight i and volume j

    for i in range(1, n+1): # for each fruit
        w, v, val = data["f"][i-1] # weight, volume, value of the fruit
        for j in range(max_w, w-1, -1): # for each weight (min is w so won't give negative index)
            for k in range(max_v, v-1, -1): # for each volume (min is v so won't give negative index)
                dp[j][k] = max(dp[j][k], dp[j-w][k-v] + val)

    result = dp[max_w][max_v]
    # my code ends here

    # logging.info("My result :{}".format(result))
    return json.dumps(result)
