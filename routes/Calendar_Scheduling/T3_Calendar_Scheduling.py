import json
import logging

from flask import request, Response

from routes import app

# My import


logger = logging.getLogger(__name__)

@app.route('/calendar-scheduling', methods=['POST'])
def add_oil():
    lesson_requests = request.get_json()
    
    lesson_requests.sort(key=lambda x: x["potentialEarnings"], reverse=True)

    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    hours_per_day = 12

    # Initialize earnings and schedule dictionaries
    earnings = 0
    schedule = {day: [] for day in days}

    # Create a dynamic programming table to store the maximum earnings
    dp_table = [[0] * (hours_per_day + 1) for _ in range(len(days) + 1)]

    # Fill the dynamic programming table
    for i in range(1, len(days) + 1):
        for j in range(1, hours_per_day + 1):
            # Consider the previous day's earnings
            dp_table[i][j] = dp_table[i - 1][j]

            # Check if the current lesson can be scheduled on the current day
            day_index = i - 1
            for lesson in lesson_requests:
                if days[day_index] in lesson["availableDays"] and lesson["duration"] <= j:
                    # Calculate the potential earnings if this lesson is scheduled
                    potential_earnings = dp_table[i - 1][j - lesson["duration"]] + lesson["potentialEarnings"]

                    # Update the maximum earnings and schedule if it's higher
                    if potential_earnings > dp_table[i][j]:
                        dp_table[i][j] = potential_earnings
                        schedule[days[day_index]].append(lesson["lessonRequestId"])
                        earnings = max(earnings, potential_earnings)

    logging.info({k:v for k,v in schedule.items() if v})
    response_data = json.dumps({k:v for k,v in schedule.items() if v})

    return Response(response_data, mimetype='application/json')
