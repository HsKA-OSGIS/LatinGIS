# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 13:00:42 2023

@author: Iván Simarro Agramunt
UPV, ETSIGCT
1o MASTER
"""
# Libraries
import requests
import requests.packages.urllib3
import json

# Settings
#Output
path="Backend/data/"
#Change Status Messages
def Message(text:str):
    print(text)
#Dissable warnings in console
requests.packages.urllib3.disable_warnings()
#URL to get package list
url_list = "https://transparenz.karlsruhe.de/api/3/action/package_list"
#URL to get data from package
url_package = "https://transparenz.karlsruhe.de/api/3/action/package_show?id="



nopoint=[]
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
gjson_all={}

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
                        if str(name) not in gjson_all:
                            gjson_all[str(name)] = {}
                        gjson_all[str(name)][str(json_package_data["result"]["resources"][resource]["name"])] = json_package_data["result"]["resources"][resource]["url"]
                try:    
                    if gjson_data["features"][0]["geometry"]["type"]!="Point":
                        nopoint.append(name)
                except:
                    continue
                Message(f'Data "{name}" obtained')

Message(f'\n  ✓ Step 2 finished.\nNumber of items {len(gjson_all)}\n ')

Message("\n  ■ Step 3: Saving all data.\n")
with open(path+"all.json", 'w') as archivo:
    json.dump(gjson_all, archivo, indent=2)
archivo.close()
Message(f'\n  ✓ Step 3 finished.\nAll Data saved in {path+"all.json"}\n ')


Message("\n  ■ Step 4: Saving tourism data.\n")
with open(path+"tourism.csv", 'w',encoding='utf-8') as archivo:
    archivo.write(f'Libraries/Archives\t{gjson_all["points-of-interest-kultur1"]["Bibliotheken / Archive"]}')
    archivo.write("\n")
    archivo.write(f'Clubs/venues\t{gjson_all["points-of-interest-kultur1"]["Clubs / Locations"]}')
    archivo.write("\n")
    archivo.write(f'Gastronomy\t{gjson_all["points-of-interest-kultur1"]["Gastronomie"]}')
    archivo.write("\n")
    archivo.write(f'Cinemas\t{gjson_all["points-of-interest-kultur1"]["Kinos"]}')
    archivo.write("\n")
    archivo.write(f'Churches/faith communities\t{gjson_all["points-of-interest-kultur1"]["Kirchen / Glaubensgemeinschaften"]}')
    archivo.write("\n")
    archivo.write(f'Cultural centers\t{gjson_all["points-of-interest-kultur1"]["Kulturzentren"]}')
    archivo.write("\n")
    archivo.write(f'Museums/exhibitions\t{gjson_all["points-of-interest-kultur1"]["Museen / Ausstellungen"]}')
    archivo.write("\n")
    archivo.write(f'Theatre\t{gjson_all["points-of-interest-kultur1"]["Theater"]}')
    archivo.write("\n")
    archivo.write(f'Venues and markets\t{str(gjson_all["points-of-interest-kultur1"]["Veranstaltungsorte und Märkte"])}')
    archivo.write("\n")
    archivo.write(f'Camping {gjson_all["points-of-interest-tourismus1"]["Camping"]}')
    archivo.write("\n")
    archivo.write(f'Hotels/Accommodations\t{gjson_all["points-of-interest-tourismus1"]["Hotels / Unterkünfte"]}')
    archivo.write("\n")
    archivo.write(f'Sightseeing features\t{str(gjson_all["points-of-interest-tourismus1"]["Sehenswürdigkeiten"])}')
    archivo.write("\n")
    archivo.write(f'Tourism offices\t{gjson_all["points-of-interest-tourismus1"]["Tourismusbüros"]}')
archivo.close()
Message(f'\n  ✓ Step 4 finished.\Tourism Data saved in {path+"tourism.csv"}\n ')



Message("\n  ■ Step 5: Saving public data.\n")
with open(path+"public.csv", 'w',encoding='utf-8') as archivo:
    archivo.write(f'Police stations\t{gjson_all["points-of-interest-behorden-und-offentliche-einrichtungen1"]["Polizeireviere"]}')
    archivo.write("\n")
    archivo.write(f'Municipal authorities\t{gjson_all["points-of-interest-behorden-und-offentliche-einrichtungen1"]["Städtische Behörden"]}')
    archivo.write("\n")
    archivo.write(f'Animal shelters\t{gjson_all["points-of-interest-behorden-und-offentliche-einrichtungen1"]["Tierheime"]}')
    archivo.write("\n")
    archivo.write(f'Public toilets\t{gjson_all["points-of-interest-behorden-und-offentliche-einrichtungen1"]["Öffentliche Toiletten"]}')
    archivo.write("\n")
    archivo.write(f'Banks / EC machines\t{gjson_all["points-of-interest-dienstleistungen1"]["Banken / EC-Automaten"]}')
    archivo.write("\n")
    archivo.write(f'Mailboxes (yellow mail)\t{gjson_all["points-of-interest-dienstleistungen1"]["Briefkästen (gelbe Post)"]}')
    archivo.write("\n")
    archivo.write(f'Post offices (yellow post office)\t{gjson_all["points-of-interest-dienstleistungen1"]["Postfilialen (gelbe Post)"]}')
    archivo.write("\n")
    archivo.write(f'Nursing homes\t{gjson_all["points-of-interest-senioren1"]["Pflegeheime"]}')
    archivo.write("\n")
    archivo.write(f'Pharmacies\t{gjson_all["points-of-interest-gesundheit-und-beratungsstellen1"]["Apotheken"]}')
    archivo.write("\n")
    archivo.write(f'Clinics\t{gjson_all["points-of-interest-gesundheit-und-beratungsstellen1"]["Kliniken"]}')
    archivo.write("\n")
    archivo.write(f'Train stations\t{gjson_all["points-of-interest-offentlicher-nahverkehr-opnv1"]["Bahnhöfe"]}')
    archivo.write("\n")
    archivo.write(f'Stops\t{gjson_all["points-of-interest-offentlicher-nahverkehr-opnv1"]["Haltestellen"]}')
archivo.close()
Message(f'\n  ✓ Step 5 finished.\Public Data saved in {path+"public.csv"}\n ')



Message("\n  ■ Step 6: Saving sports data.\n")
with open(path+"sports.csv", 'w',encoding='utf-8') as archivo:
    archivo.write(f'Volleyball courts\t{gjson_all["points-of-interest-sportanlagen1"]["Volleyballfelder"]}')
    archivo.write("\n")
    archivo.write(f'Skate / BMX courts\t{gjson_all["points-of-interest-sportanlagen1"]["Skate- / BMX-Plätze"]}')
    archivo.write("\n")
    archivo.write(f'Sports halls\t{gjson_all["points-of-interest-sportanlagen1"]["Sporthallen"]}')
    archivo.write("\n")
    archivo.write(f'Sports clubs\t{gjson_all["points-of-interest-sportanlagen1"]["Sportvereine"]}')
    archivo.write("\n")
    archivo.write(f'Basketball courts\t{gjson_all["points-of-interest-sportanlagen1"]["Basketballplätze"]}')
    archivo.write("\n")
    archivo.write(f'Football pitches/ball playing areas\t{gjson_all["points-of-interest-sportanlagen1"]["Bolzplätze / Ballspielflächen"]}')
archivo.close()
Message(f'\n  ✓ Step 5 finished.\Sports Data saved in {path+"sports.csv"}\n ')



Message("\n  ■ Step 7: Saving education data.\n")
with open(path+"education.csv", 'w',encoding='utf-8') as archivo:
    archivo.write(f'Facilities for students\t{gjson_all["points-of-interest-hochschulen-und-forschung1"]["Einrichtungen für Studenten"]}')
    archivo.write("\n")
    archivo.write(f'Research institutions\t{gjson_all["points-of-interest-hochschulen-und-forschung1"]["Forschungseinrichtungen"]}')
    archivo.write("\n")
    archivo.write(f'Colleges/Universities\t{gjson_all["points-of-interest-hochschulen-und-forschung1"]["Hochschulen / Universitäten"]}')
    archivo.write("\n")
    archivo.write(f'Youth facilities\t{gjson_all["points-of-interest-kinder-und-jugendliche1"]["Jugendeinrichtungen"]}')
    archivo.write("\n")
    archivo.write(f'kindergartens\t{gjson_all["points-of-interest-kinder-und-jugendliche1"]["Kindergärten"]}')
    archivo.write("\n")
    archivo.write(f'Daycare centers\t{gjson_all["points-of-interest-kinder-und-jugendliche1"]["Kindertagesstätten"]}')
    archivo.write("\n")
    archivo.write(f'primary schools\t{gjson_all["points-of-interest-schulen1"]["Grundschulen"]}')
    archivo.write("\n")
    archivo.write(f'secondary schools\t{gjson_all["points-of-interest-schulen1"]["Realschulen"]}')
    archivo.write("\n")
    archivo.write(f'School kindergartens\t{gjson_all["points-of-interest-schulen1"]["Schulkindergärten"]}')
    archivo.write("\n")
    archivo.write(f'Secondary schools\t{gjson_all["points-of-interest-schulen1"]["Werkrealschulen"]}')    
archivo.close()
Message(f'\n  ✓ Step 7 finished.\Education Data saved in {path+"education.csv"}\n ')
# archivo.write(f'Library {gjson_all["aa"]["bb"]}')
# archivo.write("\n")


















