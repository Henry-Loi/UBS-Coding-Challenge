import json
import logging

from flask import request

from routes import app

# My import
# import functools

# @functools.lru_cache
# def dp(i, j):
#     return dp[i][j]

logger = logging.getLogger(__name__)

@app.route('/greedymonkey', methods=['POST'])
def testing():
    data = request.get_json()
    # logging.info("data sent for evaluation {}".format(data))
    
    # my code starts here
    n, max_w, max_v = len(data["f"]), data["w"], data["v"]

    # try try top down dp
    dp = [[0]*(max_v+1) for _ in range(max_w+1)] # dp[i][j] is the max val for weight i and volume j

    for i in range(1, n+1): # for each fruit
        w, v, val = data["f"][i-1] # weight, volume, value of the fruit
        for j in range(max_w, w-1, -1): # for each weight (min is w so won't give negative index)
            for k in range(max_v, v-1, -1): # for each volume (min is v so won't give negative index)
                dp[j][k] = max(dp[j][k], dp[j-w][k-v] + val)
    # my code ends here

    # logging.info("My result :{}".format(result))
    return json.dumps(dp[max_w][max_v])
