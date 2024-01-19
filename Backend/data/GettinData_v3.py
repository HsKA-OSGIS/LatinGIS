# -*- coding: utf-8 -*-
"""
Created on Wed Dec 1 13:00:42 2023

@author: Iván Simarro Agramunt
UPV, ETSIGCT; HKA, Geomatics
2o MASTER
"""
# Libraries
import requests
import requests.packages.urllib3
import json

# Settings
#Output
path="Backend/data/data.json"
#Change Status Messages
def Message(text:str):
    print(text)
#Dissable warnings in console
requests.packages.urllib3.disable_warnings()
#URL to get package list
url_list = "https://transparenz.karlsruhe.de/api/3/action/package_list"
#URL to get data from package
url_package = "https://transparenz.karlsruhe.de/api/3/action/package_show?id="




#                  CODE

Message("\n  ■ Step 1: Getting package list.\n")
try:
    # Request for the list
    response = requests.get(url_list)

    # Verify
    if response.status_code == 200:
        # Get data
        json_data = response.json()
    else:
        # Error Message
        Message(f"Error al obtener la URL. Código de estado: {response.status_code}")

except Exception as e:
    # Error in URL
    Message(f"Error: {e}")
    quit()

Message(f'  ✓ Step 1 finished.\nNumber of items {len(json_data["result"])}\n ')

# GET PACKAGE LIST

# test & dicc
gjson_e={}

for name in json_data["result"]:
    # Request for data
    response = requests.get(url_package+name)
    # Verify
    if response.status_code == 200:
        # Get data
        json_package_data = response.json()
        # Filter: existance of data
        if json_package_data["result"]["resources"]:
            # Filter: package with GeoJSON data
            if json_package_data["result"]["resources"][0]["format"]=="GeoJSON":
                # Requesting for each data in package
                for resource in range(int(json_package_data["result"]["num_resources"])):
                    # Getting the URL for data
                    url_gjson = f'{json_package_data["result"]["resources"][resource]["url"]}'
                    # Filter: URL is for GeoJSON data
                    if url_gjson[-4:] == "json":
                        # Filter: Broken URLs
                        try:
                            # Request for GeoJSON data
                            response = requests.get(url_gjson, verify=False)
                            # Get data
                            gjson_data = response.json()
                        except:
                            break
                        # Create new diccionary or not
                        if str(name) not in gjson_e:
                            gjson_e[str(name)] = {}
                        gjson_e[str(name)][str(json_package_data["result"]["resources"][resource]["name"])] = json_package_data["result"]["resources"][resource]["url"]
                Message(f'Data "{name}" obtained')

Message(f'\n  ✓ Step 2 finished.\nNumber of items {len(gjson_e)}\n ')

Message("\n  ■ Step 3: Saving data.\n")
with open(path, 'w') as archivo:
    json.dump(gjson_e, archivo, indent=2)
Message(f'\n  ✓ Step 3 finished.\nData saved in {path}\n ')