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

# TODO: Create constants for debugging levels - Replace for an actual logger
menu_options = 0    # User selection


"""
    Use a partial or full vehicle name or model to get
    a list of pilots associated with the vehicle plus
    a list of the matched results with no associated pilot
    Using the requests python lib
"""
def get_vehicle_info(keyword):
    global menu_options
    print("Searching Vehicles and models that match: " + "\"" + keyword + "\"")

    """
        Hold the results already filtered
    """
    results = {
        # With Pilots  "with_pilots":["name", "pilots"]
        "with_pilots":[],  
        "without_pilots":[]
    }

    r = requests.get("https://swapi.dev/api/vehicles/?") # Get all vehicle data available 
    json_query_results = r.json() # Extract in JSON format

    if (menu_options == '2'):
        print("\nAll Results")
    for res in json_query_results['results']: # Go through all results
        if (menu_options == '2'):
            print(res)                        # Display all resutls for debugging
        
        """
        **********************************************************************
            Check if there is a match with the keyword the user selected
        **********************************************************************
        """
        name = res['name']
        model = (res['model'])

        if (res['name'].find(keyword) != -1 or res['model'].find(keyword) != -1): # Check if the keyword matches a name or model

            """
            **********************************************************************
                There is a match - Check for the pilot's information
            **********************************************************************
            """
            if (res["pilots"]): # Check if there is a pilot associated

                #num_pilots = len(res["pilots"])
                #for x in range(num_pilots): # Iterate through pilot key values and get the associated info
                p_name = get_pilot_information(res["pilots"]) # Get the info of the associated pilots
                match = {"name": name, "pilots": p_name}
                results['with_pilots'].append(match)
            else:
                results['without_pilots'].append(name) # Append only vehicle name to the dictionary        
        else:
            if (menu_options == '2'):
                print("\nNo keyword match\n")

    """
    Display the results
    """
    print("Results\n")
    print(results)

"""
    Get the name of the pilot using API pilot endpoint
    Called by get_vehicle info
"""
def get_pilot_information(pilot_query):
    global menu_options
    if (menu_options == '2'):
        print("\nGetting pilot info: " + str(pilot_query))
    pilots = []                     # List to hold the pilot's name if more than 1 is associated to a vehicle
    num_pilots = len(pilot_query)
    for x in range(num_pilots):
        if (menu_options == '2'):
            print("\nQuerying: " + str(pilot_query[x]))
        json_pilot_info = requests.get(pilot_query[x]).json() # Process one GET request at the tiem
        pilots.append(json_pilot_info['name'])                # Add the name to the list

    if (menu_options == '2'):
        print(pilots)

    return pilots

def menu():
    print("Versature client")
    global menu_options
    print("Select one of the options below")
    print("1. Basic client exercise")
    print("2. Debug client exercise")
    print("3. Custom search")
    menu_options = input("Selection: ")

"""
    Program entry point
"""
if __name__ == "__main__":
    menu()
    get_vehicle_info("AT-")
    pass