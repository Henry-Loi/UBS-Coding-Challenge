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

@app.route('/calendar-scheduling', methods=['POST'])
def add_oil():
    lesson_requests = request.get_json()
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
            
    return json.dumps({k:v for k,v in schedule.items() if v})
