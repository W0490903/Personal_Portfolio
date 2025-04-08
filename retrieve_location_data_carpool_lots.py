import googlemaps
import csv
from pathlib import Path

# API key
api_key = 'AIzaSyDiZeoCk5xpIbrjSd83ntur4gFuOqpqNig'

# Initialize the Google Maps client
gmaps = googlemaps.Client(key=api_key)

# List of addresses to search.
addresses = [
    # Add your addresses here.
    # 'Address 1', 'Address 2', ...
    '199 Main St W, Hardwood Lands NS B0N 1Y0',  # 1
    '16 W Brookfield Cemetery Rd, Brookfield, NS B0N 1C0',  # 2
    '86 Connector Rd Hwy 102S Exit 13, Truro NS B2N 5B6',  # 3
    '772 Salt Springs Rd Springhill, NS B0M 1X0',  # 4
    '709 Pictou Rd, Valley NS B6L 2P3',  # 5
    '831 Old Coach Rd, Salt Springs NS B0K 1P0',  # 6
    '125 School Rd, Thorburn NS B0K 1W0',  # 7
    'Exit 6 Carpool Lot, Hubbards NS B0J 1T0',  # 8
    '2251 Lighthouse Rte, Chester NS B0J 1T0',  # 9
    'Exit 8 Carpool Lot, Chester NS',  # 10
    'Exit 9 Car Pool Parking Lot Chester Basin Nova Scotia',  # 11
    '8364 Lighthouse Rte Halifax, NS',  # 12
    '180 Langille Lake Rd Halifax, NS',  # 13
    '14 Cooks Ln Parking, Cookville NS B4V 7P5',  # 14
    'Exit 13 Car Pool Parking Lot, Wileville NS',  # 15
    'Car Pool Parking Lot, Port Medway Rd, Mill Village NS B0J 2H0',  # 16
    'Exit 19 Car Pool Parking Lot Liverpool NS',  # 17
    'Car Pool Parking Lot, 96 Ohio Rd, Shelburne, NS B0T 1W0',  # 18
    'Exit 31 Car Pool Parking Lot, Pubnico NS',  # 19
    '5679 Chemin Old Oak Rd, Glenwood NS B0W 1W0',  # 20
    '316 Gavel Rd, Tusket NS B0W 3M0',  # 21
    'Salmon River Rd Car Pool Salmon River NS',  # 22
    '764 Little Brook Rd Parking, Little Brook NS',  # 23
    'Carpool Parking Lot Trunk 8, Annapolis Royal, NS',  # 24
    '52 Schofield Rd Parking, Kentville NS',  # 25
    '5435 Prospect Rd Parking, New Minas NS',  # 26
    '2186 Gaspereau River Rd Parking, Avonport NS',  # 27
    '519 Ben Jackson Rd Parking, Hantsport NS',  # 28
    '79 Evangeline Trail Parking, Mt. Uniacke NS',  # 29
    'Rocks Rd Parking, St. Croix NS',  # 30
    'Park & Ride Windsor, Windsor NS',  # 31
    '68 Grant Rd Parking, Hardwood Lands NS B0N 1Y0',  # 32
    '294 NS-214, Elmsdale NS B2S 2K9',  # 33
    'Milford Carpool, Milford NS',  # 34
    '1311 Prospect Rd Parking, Beechville NS',  # 35
    '44.78344109779389, -63.16651012716467, Musquodoboit Harbour NS',  # 36
    '18 Heritage View Dr Parking, Chezzetcook NS',  # 37
    'Hwy 7 Before William Porter Connector (9078), Porters Lake NS',  # 38
    '168 Mineville Rd Parking, Halifax NS',  # 39
    'Car Pool Parking Lot Whiteside Road, Louisdale NS',  # 40
    '1467 George Street, Mira Road NS'  # 41
]

# List of manually defined stop names (the same length as the addresses list)
# If only one stop name is entered, all addresses will use that name.
stop_names = [
    # Apply specific stop names for each address.
    # 'Stop Name 1', 'Stop Name 2', ...
    'Highway 102, Exit 11 at Stewiacke',  # 1
    'Highway 102, Exit 12 at Brookfield',  # 2
    'Highway 102, Exit 13 at Truro',  # 3
    'Highway 104, Exit 5 at Springhill',  # 4
    'Highway 104, Exit 17 at Valley',  # 5
    'Highway 104, Exit 19 at Salt Springs',  # 6
    'Highway 104, Exit 27 at Sutherlands River',  # 7
    'Highway 103, Exit 6 at Hubbards',  # 8
    'Highway 103, Exit 7 at East River',  # 9
    'Highway 103, Exit 8 at Chester',  # 10
    'Highway 103, Exit 9 at Chester Basin',  # 11
    'Highway 103, Exit 10 at Oakland',  # 12
    'Highway 103, Exit 11 at Blockhouse',  # 13
    'Highway 103, Exit 12 at Cookville',  # 14
    'Highway 103, Exit 13 at Wileville ',  # 15
    'Highway 103, Exit 17A at Mill Village ',  # 16
    'Highway 103, Exit 19 at Liverpool',  # 17
    'Highway 103, Exit 26 at Shelburne',  # 18
    'Highway 103, Exit 31 at Pubnico',  # 19
    'Highway 103, Exit 32A at Glenwood',  # 20
    'Highway 103, Exit 33 at Tusket',  # 21
    'Highway 101, Exit 32 at Lake Doucette',  # 22
    'Highway 101, Exit 29 at Little Brook',  # 23
    'Highway 101, Exit 22 at Greywood (Trunk 8)',  # 24
    'Highway 101, Exit 13 at Kentville',  # 25
    'Highway 101, Exit 12 at New Minas',  # 26
    'Highway 101, Exit 9 at Avonport ',  # 27
    'Highway 101, Exit 8A at Ben Jackson Road',  # 28
    'Highway 101, Exit 3 at Mt. Uniacke',  # 29
    'Highway 101, Exit 4 at St. Croix',  # 30
    'Highway 101, Exit 6 at Windsor',  # 31
    'Highway 102, Exit 7, at Enfield',  # 32
    'Highway 102, Exit 8 at Elmsdale',  # 33
    'Highway 102, Exit 9 at Milford',  # 34
    'Route 333, Beechville',  # 35
    'Trunk 7, Musquodoboit Harbour',  # 36
    'Trunk 7, East Chezzetcook',  # 37
    'Trunk 7, Porters Lake',  # 38
    'Mineville Road at Highway 107',  # 39
    'Intersection of Route 320 and Whiteside Road',  # 40
    'Intersection of Highway 125 and Trunk 22'  # 41
]


# File path.
csv_file_path = Path('stops.csv')

stop_id_start = 3000

# Open the CSV file and read existing entries into a set for faster lookups.
existing_entries = set()
all_rows = []

if csv_file_path.exists():
    with open(csv_file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip header row
        for row in reader:
            existing_entries.add(row[2].strip())  # Stop description is in the third column
            all_rows.append(row)  # Add the rows to the list to sort them later

    # Set the initial stop_id to the defined start point
    stop_id = stop_id_start  # Start appending with the determined stop_id

    # Search each address and append the result if it's not a duplicate.
    for idx, address in enumerate(addresses):
        try:
            geocode_result = gmaps.geocode(address)

            # Debug: Print the full geocode result to see what's being returned
            # print(f"Geocode result for {address}: {geocode_result}")

            if geocode_result:
                # Extract address components.
                address_components = geocode_result[0]['address_components']
                
                # Loop through the address components to find street_name (route) and locality (town)
                for component in address_components:
                    if 'route' in component['types']:
                        street_name = component.get('short_name', 'N/A')
                    elif 'locality' in component['types']:
                        town = component.get('long_name', 'N/A')

                # Get stop name from the list based on the index.
                # Apply the same stop name for all addresses if only one stop name is provided.
                if len(stop_names) != 0:
                    stop_name = stop_names[0] if len(stop_names) == 1 else stop_names[idx]
                else:
                    stop_name = f"{street_name} {town}" # If no stop name in the list exists, stop name is equal to the specified string.
                
                # Initialize variables for address parts
                stop_desc_parts = []
                
                for component in address_components:
                    value = None

                    if 'street_number' in component['types']:
                        value = component.get('short_name', None)  # Get street_number if available
                    elif 'route' in component['types']:
                        value = component.get('short_name', None)  # Get route if available
                    elif 'locality' in component['types']:
                        value = component.get('long_name', None)  # Get locality if available
                    elif 'administrative_area_level_1' in component['types']:
                        value = component.get('long_name', None)  # Get administrative_area_level_1 if available
                    elif 'postal_code' in component['types']:
                        value = component.get('short_name', None)  # Get postal_code if available

                    # Only append valid values (not None or 'N/A')
                    if value and value != 'N/A':
                        stop_desc_parts.append(value)

                # Combine address information into one string for the 'stop_desc' field
                stop_desc = ' '.join(stop_desc_parts)

                # Get latitude from returned data.
                latitude = geocode_result[0]['geometry']['location']['lat']
                # Get longitude from returned data.
                longitude = geocode_result[0]['geometry']['location']['lng']        

                # Combine address information into one string for the 'stop_desc' field
                stop_desc = ' '.join(stop_desc_parts)

                # Variable to add the zone ID.
                zone_id = None

                # Variable to add the stop URL.
                stop_url = None

                # Check if the stop id and stop name are already in the set of existing entries
                if stop_desc not in existing_entries:
                    all_rows.append([stop_id, stop_name, stop_desc, latitude, longitude, zone_id, stop_url]) # Create a row (record) for each address.
                    existing_entries.add(stop_desc)  # Add to existing entries to prevent future duplicates
                    stop_id += 1 # Increment stop_id for the next entry
                    print(f"Appended: {stop_id}, {stop_name}")
                else:
                    print(f"Duplicate found, skipping: {stop_id}, {stop_name}")
            else:
                print(f"No results found for address: {address}")

        except googlemaps.exceptions.ApiError as e:
            print(f"Google Maps API error while geocoding {address}: {e}")
        except Exception as e:
            print(f"Unexpected error while geocoding {address}: {e}")

# After writing the new data, now we sort the rows by stop_id
all_rows.sort(key=lambda x: int(x[0]))  # Sort by the first column (stop_id) as an integer

# Open the CSV file to write the sorted rows
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header again
    writer.writerow(['stop_id', 'stop_name', 'stop_desc', 'stop_lat', 'stop_lon', 'zone_id', 'stop_url'])
    
    # Write the sorted rows
    writer.writerows(all_rows)
