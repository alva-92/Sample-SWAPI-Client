"""
    This file is part of Sample-SWAPI-Client which is released under an GNU GPLv3 License.
    See file README or go to LICENSE for full license details.

    @name         client.py
    @description  This program initializes a client to the Star Wars API (SWAPI)
    @author       Gerardo Enrique Alvarenga
    @version      1.1
"""

import requests
import json

# TODO: Create constants for debugging levels - Replace for an actual logger
menu_options         = 0    # User selection
menu_advance_options = 0    # User selection
user_search          = ""   # Keyword the user is looking for
counter              = 0

"""
Supported Endpoints
"""
VEHICLES_ENDPOINT = "https://swapi.dev/api/vehicles/?"
DRIVERS_ENDPOINT  = "https://swapi.dev/api/people/?"

"""
    Use a partial or full vehicle name or model to get
    a list of pilots associated with the vehicle plus
    a list of the matched results with no associated pilot
    Using the requests python lib
"""
def get_vehicle_info(keyword):
    global menu_options
    global counter

    print("Searching Vehicles and models that match: " + "\"" + keyword + "\"")

    """
        Hold the results already filtered
    """
    results = {
        "count":"",
        # With Pilots  "with_pilots":["name", "pilots"]
        "with_pilots":[],  
        "without_pilots":[]
    }

    r = requests.get(VEHICLES_ENDPOINT) # Get all vehicle data available 
    json_query_results = r.json()       # Extract in JSON format

    if (menu_options == 2):
        print("\nAll Results")
    for res in json_query_results['results']: # Go through all results
        if (menu_options == 2):
            print(res)                        # Display all resutls for debugging
        
        """
        **********************************************************************
            Check if there is a match with the keyword the user selected
        **********************************************************************
        """
        name = res['name']
        model = res['model']

        if (res['name'].lower().find(keyword.lower()) != -1 or res['model'].lower().find(keyword.lower()) != -1): # Check if the keyword matches a name or model

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
                # There was no pilot information found
                results['without_pilots'].append(name) # Append only vehicle name to the dictionary

            counter += 1  
            
        else:
            if (menu_options == 2):
                print("\nNo keyword match\n")

    """
    Display the results
    """
    results['count'] = (counter)
    print("Results\n")
    print(results)
    counter = 0 # Reset counter

"""
    Get the name of the pilot using API pilot endpoint
    Called by get_vehicle info
"""
def get_pilot_information(pilot_query):
    global menu_options
    if (menu_options == 2):
        print("\nGetting pilot info: " + str(pilot_query))
    pilots = []                     # List to hold the pilot's name if more than 1 is associated to a vehicle
    num_pilots = len(pilot_query)
    for x in range(num_pilots):
        if (menu_options == 2):
            print("\nQuerying: " + str(pilot_query[x]))
        json_pilot_info = requests.get(pilot_query[x]).json() # Process one GET request at the tiem
        pilots.append(json_pilot_info['name'])                # Add the name to the list

    if (menu_options == 2):
        print(pilots)

    return pilots

"""
    Get the profile of the selected driver using search parameter provided
    by the SWAPI instead of the filter we were using for the vehicle
"""
def get_full_driver_profile(pilot_name):
    global menu_options
    profile = {
        "Driver":[]
    }
    if (menu_options == 2):
        print("\nGetting pilot info: " + str(pilot_name))

    driver = requests.get(DRIVERS_ENDPOINT +"search="+pilot_name).json() 
    for res in driver['results']: # Go through all results
        profile["Driver"].append(res['name'])
        profile["Driver"].append(res['height'])
        profile["Driver"].append(res['hair_color'])
        profile["Driver"].append(res['skin_color'])
        profile["Driver"].append(res['eye_color'])
        profile["Driver"].append(res['birth_year'])

    return profile
    
"""
    Display options to the user and prompt for a keyword to look for in the SWAPI DB
"""
def menu():
    print("\nVersature client\n")
    global menu_options
    global user_search
    while(1):
        print("Select one of the options below")
        print("1. Basic client exercise")
        print("2. Debug client exercise")
        print("3. Custom search")
        print("4. Exit")

        try:    
            menu_options = int(input("\nSelection: "))
            if (menu_options == 4):
                print("Bye...")
                exit(0)

            elif (menu_options == None or menu_options < 0 or menu_options > 4):
                print("Invalid input")
                break

            user_search = input("Enter keyword to search for: ")
        
            if (user_search == None):
                print("Invalid input")
            else:
                get_vehicle_info(user_search)
                advance_menu()
                # TODO: Should do some better input validation - make sure that input is safe - No injections, symbols, etc.
                print("\n")

        except ValueError:
            print("Invalid input")
            break

"""
    Second menu which allows the user to search for the profile of the driver
    @TODO: Needs error handling
"""
def advance_menu():
    global menu_advance_options
    print("\nSelect one of the custom search categories below")
    print("1. Search pilot profile")
    print("2. Run another search")
    menu_advance_options = int(input("\nSelection: "))
    if (menu_advance_options == 1):
        pilot_search = input("Enter the pilot name: ")
        pilot_res = get_full_driver_profile(pilot_search)
        print(pilot_res)

    elif (menu_advance_options == 2):
        menu()

"""
    Program entry point
"""
if __name__ == "__main__":
    menu()
    pass