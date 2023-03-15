import json


def create_route():
    with open("/home/ubuntu/output/coordinates_hotel.json") as f1:
        hotels = json.load(f1)
    with open("/home/ubuntu/output/coordinates_train.json") as f2:
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

    # Save the routes dictionary to a JSON file
    with open("/home/ubuntu/output/routes.json", "w") as f3:
        json.dump(routes, f3, indent=4)

    return routes