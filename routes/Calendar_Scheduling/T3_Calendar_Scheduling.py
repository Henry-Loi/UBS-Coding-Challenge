import json
import logging

from flask import request, Response

from routes import app

# My import


logger = logging.getLogger(__name__)

@app.route('/calendar-scheduling', methods=['POST'])
def add_oil():
    lesson_requests = request.get_json()
    
    logging.info("data sent for evaluation {}".format(lesson_requests))

    schedule = {}
    earnings = 0

    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    hours_per_day = 12

    # Sort lesson requests in descending order of potential earnings
    lesson_requests.sort(key=lambda x: x["potentialEarnings"], reverse=True)

    # Initialize schedule for each day
    for day in days:
        schedule[day] = []

    # Schedule lessons
    for lesson in lesson_requests:
        duration = lesson["duration"]
        potential_earnings = lesson["potentialEarnings"]
        available_days = lesson["availableDays"]

        # Find the first available day with enough hours to schedule the lesson
        for day in available_days:
            if sum(len(schedule[d]) for d in available_days) + duration <= hours_per_day:
                schedule[day].append(lesson["lessonRequestId"])
                earnings += potential_earnings
                break

    logging.info({k:v for k,v in schedule.items() if v})
    response_data = json.dumps({k:v for k,v in schedule.items() if v})

    return Response(response_data, mimetype='application/json')
