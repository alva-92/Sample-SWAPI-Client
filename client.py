"""
    This file is part of Sample-SWAPI-Client which is released under an GNU GPLv3 License.
    See file README or go to LICENSE for full license details.

    @name         client.py
    @description  This program initializes a client to the Star Wars API (SWAPI)
    @author       Gerardo Enrique Alvarenga
    @version      1.0
"""

import requests
import json

"""
    Use a partial or full vehicle name or model to get
    a list of pilots associated with the vehicle plus
    a list of the matched results with no associated pilot
    Using the requests python lib
"""
def get_vehicle_info(keyword):
    print("Searching records that match " + keyword)

    r = requests.get("https://swapi.dev/api/vehicles/?") # Get all vehicle data available 
    print(r.content)


def menu():
    print("Versature client")


"""
    Program entry point
"""
if __name__ == "__main__":
    menu()
    get_vehicle_info("AT-")
    pass