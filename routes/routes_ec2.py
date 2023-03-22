import json


def create_route():
    print('Loading hotel coordinates from coordinates_hotel.json')
    with open("/home/ubuntu/output/coordinates_hotel.json") as f1:
        hotels = json.load(f1)
    print('Loaded hotel coordinates successfully')

    print('Loading train coordinates from coordinates_train.json')
    with open("/home/ubuntu/output/coordinates_train.json") as f2:
        trains = json.load(f2)
    print('Loaded train coordinates successfully')

    routes = {}
    route_num = 1
    for train_name, train_coord in trains.items():
        for hotel_name, hotel_coord in hotels.items():
            route_key = int(route_num)
            route_value = {
                "start_coordinate": train_coord,
                "end_coordinate": hotel_coord,
            }
            routes[route_key] = route_value
            route_num += 1

    print('Creating output directory /home/ubuntu/output/routes.json if it does not exist')
    os.makedirs("/home/ubuntu/output", exist_ok=True)

    # Save the routes dictionary to a JSON file
    print('Saving routes to /home/ubuntu/output/routes.json')
    with open("/home/ubuntu/output/routes.json", "w") as f3:
        json.dump(routes, f3)
    print('Saved routes successfully')

    print('Printing the first three lines of /home/ubuntu/output/routes.json')
    # Print the first three lines of the routes.json file
    with open("/home/ubuntu/output/routes.json") as f4:
        for i in range(3):
            print(f4.readline(), end="")

    return routes

