import json

def create_route():
    with open("/coordinates_hotel.json") as f1:
        hotels = json.load(f1)
    with open("/coordinates_train.json") as f2:
        trains = json.load(f2)
    routes = {}
    for train_name, train_coord in trains.items():
        for hotel_name, hotel_coord in hotels.items():
            route_key = f"route_{len(routes) + 1}"
            route_value = {
                "start_coordinate": train_coord,
                "end_coordinate": hotel_coord,
            }
            routes[route_key] = route_value
    return routes

