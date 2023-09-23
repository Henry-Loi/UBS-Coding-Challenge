import json
import logging

from flask import request, Response

from routes import app

# My import


logger = logging.getLogger(__name__)

@app.route('/parking-lot', methods=['POST'])
def calculate_parking_assignment():
    data = request.get_json()
    # logging.info("data sent for evaluation {}".format(data))
    
    # my code starts here
    bus_parking_slots = data['BusParkingSlots']
    car_parking_slots = data['CarParkingSlots']
    parking_charges = data['ParkingCharges']
    buses = data['Buses']
    cars = data['Cars']
    bikes = data['Bikes']

    bus_rejections = max(buses - bus_parking_slots, 0)
    car_rejections = max(cars - car_parking_slots, 0)
    bike_rejections = max(bikes - (bus_parking_slots * 2 + car_parking_slots * 5), 0)

    if bus_rejections > 0:
        bus_replacement_options = [
            (2, 2, 0),  # Replace 1 Bus park with 2 Cars park + 2 Bikes park
            (2, 0, 0),  # Replace 1 Bus park with 2 Cars park
            (1, 7, 0),  # Replace 1 Bus park with 1 Car park + 7 Bikes park
            (0, 12, 0)  # Replace 1 Bus park with 12 Bikes park
        ]

        for option in bus_replacement_options:
            cars_needed, bikes_needed, _ = option

            while bus_rejections > 0 and cars_needed <= cars and bikes_needed <= bikes:
                cars -= cars_needed
                bikes -= bikes_needed
                bus_rejections -= 1

    profit = (bus_parking_slots * parking_charges['Bus']) + (car_parking_slots * parking_charges['Car']) + (bikes * parking_charges['Bike'])

    result = {
        'Profit': profit,
        'BusRejections': bus_rejections,
        'CarRejections': car_rejections,
        'BikeRejections': bike_rejections
    }

    response_data = json.dumps({'Answer': result})
    # my code ends here
    
    # logging.info("My result :{}".format(result)
    return Response(response_data, mimetype='application/json')
