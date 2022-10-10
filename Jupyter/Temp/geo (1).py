"""
Python module for geo-location.
"""
import pandas as pd
import numpy as np
import re
    
def geocode_default():
    return {'gc_geocoder':       '',
            'gc_street_address': np.nan,
            'gc_city':           np.nan,
            'gc_state':          np.nan,
            'gc_zip_code':       np.nan,
            'gc_lat':            np.nan,
            'gc_lon':            np.nan,
            'gc_confidence':     np.nan}
 
def geocode(location, method = 'progressive', autocomplete = True):
    gc = []
    if location == '':
        return geocode_default()

    if (method in ['pelias', 'all']) or (method == 'progressive'): 
        gc.append(geocode_pelias(location, autocomplete = True))
    if (method in ['nominatim', 'all']) or ( 
            (method == 'progressive') and (pd.isnull(gc[-1]['gc_confidence']) or (gc[-1]['gc_confidence'] == 0))
            ): 
        gc.append(geocode_nominatim(location))
    return gc


def geocode_nominatim(location):
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="open_street_map")
    
    if isinstance(location, dict):
        location = f"{location['gc_street_address']} {location['gc_city']} {location['gc_state']} {location['gc_zip_code']}"
    
    gc = geocode_default()
    gc['gc_geocoder'] = 'nominatim'
    if location == '':
        return gc

    try:
        response = geolocator.geocode(location, addressdetails = True)
        #print(response.raw)
        gc['gc_lat']            = response.latitude
        gc['gc_lon']            = response.longitude
        gc['gc_confidence']     = 0.0 
        if 'house_number' in response.raw['address'].keys():
            gc['gc_street_address'] = response.raw['address']['house_number'] + ' ' + response.raw['address']['road'].upper()
        elif 'shop' in response.raw['address'].keys():
            gc['gc_street_address'] = response.raw['address']['shop'].upper() + ' ' + response.raw['address']['road'].upper()
        elif 'leisure' in response.raw['address'].keys():
            gc['gc_street_address'] = response.raw['address']['leisure'].upper()
        else:
            gc['gc_street_address'] = ''
        
        if 'city' in response.raw['address'].keys():
            gc['gc_city']           = response.raw['address']['city'].upper()
        elif 'village' in response.raw['address'].keys():
            gc['gc_city']           = response.raw['address']['village'].upper()
        elif 'hamlet' in response.raw['address'].keys():
            gc['gc_city']           = response.raw['address']['hamlet'].upper()
        else:
            gc['gc_city']   = ''
            
        if 'postcode' in response.raw['address'].keys():
            gc['gc_zip_code']       = response.raw['address']['postcode']
        
        gc['gc_state']              = response.raw['address']['state'].upper()

        if (gc['gc_street_address']):
            gc['gc_confidence'] = 1.0            
        if gc['gc_state'] == 'NEW MEXICO':
            gc['gc_state'] = 'NM'     
    except:
        pass
    return gc

def geocode_pelias(location, autocomplete = True):
    import json
    import requests 
    
    if isinstance(location, dict):
        location = f"{location['gc_street_address']} {location['gc_city']} {location['gc_state']} {location['gc_zip_code']}"
    
    gc = geocode_default()
    gc['gc_geocoder'] = 'pelias'
    if location == '':
        return gc

    if autocomplete:
        url_query_string = f'http://172.30.142.49:4000/v1/autocomplete?text={location}&size=1'
    else: 
        url_query_string = f'http://172.30.142.49:4000/v1/search/?text={location}'
    
    response = requests.get(url_query_string)
    toJson = response.json()
    
    if len(toJson["features"]) > 0 and toJson["features"][0]["geometry"]["coordinates"]:
        properties = toJson["features"][0]["properties"]
        gc['gc_geocoder'] = 'pelias'
        gc['gc_lat'] = toJson["features"][0]["geometry"]["coordinates"][1]
        gc['gc_lon'] = toJson["features"][0]["geometry"]["coordinates"][0]
        try:
            gc['gc_street_address'] = properties['name'].upper()
            gc['gc_city'] = properties['locality'].upper()
            gc['gc_state'] = properties['region_a'].upper()
            gc['gc_zip_code'] = properties["postalcode"]
        except:
            pass
        if gc['gc_zip_code'] == '':
            gc['gc_confidence'] = 0.0
        elif not(any(s.isdigit() for s in gc['gc_street_address'])):
            gc['gc_confidence'] = 0.0
        elif 'gc_confidence' in properties.keys():                
            gc['gc_confidence'] = properties['confidence']
        else:
            gc['gc_confidence'] = 1.0
    
    return gc



# def geocode_df(df, input_column='Incident_Location', output_column='Incidentgc_latgc_long',
#                confidence_flag=False):
#     """ A function for bulk geocoding location data in a dataframe using Pelias.
#        Takes in a dataframe containing the location data to be geocoded.
#        Reads string location from input_column, default 'Incident_Location'
#        Returns the data frame updated with output_column, default 'Incidentgc_latgc_long'.
#        If confidence_flag is True (default False), returns confidence in 'Confidencegc_latgc_long'
#        """
#     df[output_column] = ''  # pd.NaT # should this be None (a string?)
#     for i, row in df.iterrows():
#         location = row[input_column]
#         geocodedgc_latgc_long, confidence = geocode_location(location)
#         lat = geocodedgc_latgc_long[1]
#         long = geocodedgc_latgc_long[0]
#         df.at[i, output_column] = f"{lat}, {long}"
#         if confidence_flag:
#             df.at[i, 'Confidencegc_latgc_long'] = confidence
#     return df

def validate_address(address):
    from usps import Address, USPSApi
    
    address_validated = {        
        'gc_street_address': np.nan,
        'gc_city': np.nan,
        'gc_state': np.nan,
        'gc_zip_code': np.nan,
    }
        
    query_address = Address(
                    name            = "",
                    address_1       = address['gc_street_address'],
                    city            = address['gc_city'],
                    state           = address['gc_state'],
                    zipcode         = address['gc_zip_code'],
                    )

    try:
        usps = USPSApi("050OFFIC7461", test=True)
        validation = usps.validate_address(query_address)
        response = validation.result["AddressValidateResponse"]["Address"]
        
        address_validated['gc_street_address'] = response["Address2"]
        address_validated['gc_city'] = response["City"]
        address_validated['gc_state'] = response["State"]
        address_validated['gc_zip_code'] = response["Zip5"]        
    except:
        pass

    return address_validated

        
def to_address(charge_location):
    """Reads a string and returns a dictionary"""
    
    from scourgify import normalize_address_record

    address = {        
        'gc_street_address': '',
        'gc_city': '',
        'gc_state': '',
        'gc_zip_code': '',
    }

    if charge_location == '':
        return address
    
    try:
        normalized = normalize_address_record(charge_location)
        
        if normalized['address_line_1'] == None:
            address['gc_street_address'] = charge_location
        else:
            address['gc_street_address'] = normalized['address_line_1']
        
        if (normalized['city'] == None) | (normalized['city'] == 'NEW MEXICO'):            
            address['gc_city'] = 'BERNALILLO COUNTY' 
            # 'ALBUQUERQUE'            
        else:
            address['gc_city'] = normalized['city']
        
        if normalized['state'] == None:
            address['gc_state'] = 'NM'
        else:
            address['gc_state'] = normalized['state']
        
        if normalized['postal_code'] == None:
            address['gc_zip_code'] = ''
        else:
            address['gc_zip_code'] = normalized['postal_code']
    except:
        #print('Default')
        address['gc_street_address'] = charge_location
        address['gc_city'] = 'BERNALILLO COUNTY' 
        #'ALBUQUERQUE'
        address['gc_state'] = 'NM'
        address['gc_zip_code'] = ''            
    return address

def repair_address_df(df, input_column='Incident_Location', output_column='Sanitized Address', confidence_flag=False):
    """Returns a queried version of the address. Should repair formatting, and often provides additional information."""
    import json
    import requests

    df[output_column] = ''

    for i, row in df.iterrows():
        url = f"http://172.30.142.49:4000/v1/autocomplete?text={row[input_column]}&size=1"
        response = requests.get(url)
        try:
            row[output_column] = response.json(
            )['features'][0]['properties']['label'].replace(', USA', '')
        except:
            continue
    return df


def dist_between(L1, L2):
    """Computes the distance between L1 and L2 in miles.
        L1 and L2 are tuples with (Latitude, Longitude)"""
    import geopy.distance
    import numpy as np
    if L1 == (0, 0) or L2 == (0, 0):
        return np.nan
    return geopy.distance.geodesic(L1, L2).miles


def dist_between_df(L, df, col='Incidentgc_latgc_long'):
    temp = df.copy()
    temp[['lat', 'long']] = temp[col].str.split(
        ', ', expand=True).astype(float)
    df['Dist_Miles'] = temp.apply(lambda row: dist_between(
        L, (row['lat'], row['long'])), axis=1)
    return df


def push_sql(df, table, con):
    df.to_sql(table, con=con, if_exists='replace', index=False)

    
def sanitize_location(location):
    # remove \           
    
    if pd.isnull(location):
        location = ''
        return location
    
    # remove specific pattern for APS schools
    location = re.sub(r'APS - .+ - ', '', location)
    # Remove "1/2", often included as part of address
    location = re.sub(r'\b1/2\b', '', location)
    # Remove any dates
    location = re.sub(r'\d{1,2}/\d{1,2}/\d{2,4}', '', location)
    
    # remove #, tabs, question marks, spaces
    location = re.sub(r'^#', '', location)
    location = re.sub(r'[\r\n\t-]', ' ', location)
    location = re.sub(r'[\.\?]', ' ', location)
    location = re.sub(r"'", '', location)
    location = re.sub(r' +', ' ', location)

    location = re.sub('ABQ[^\s]+', 'ALBUQUERQUE', location)
    location = re.sub('ALB[^\s]+', 'ALBUQUERQUE', location)
    
    
    # Repair street names
    location = re.sub(r'\bALMAMO\b',         'ALAMO', location)         

    location = re.sub(r'\bALMEDA\b',         'ALAMEDA', location)
    location = re.sub(r'\bALCANZAR\b',       'ALCAZAR', location)
    location = re.sub(r'\bALVARDO\b',        'ALVARADO', location)
    
    location = re.sub(r'\bATISCO\b',         'ATRISCO', location)
    location = re.sub(r'\bBUENTA\b',         'BUENA', location)
    location = re.sub(r'\bBRODWAY\b',        'BROADWAY', location)
    location = re.sub(r'\b(BRYN MAUWR|BRYNMAWR|RYAN MAWR|BRY MAWR)\b',  'BRYN MAWR', location)  
    location = re.sub(r'\bGERARD\b',         'GIRARD', location)
    location = re.sub(r'\b(GIBSOB|GIBOSN)\b',               'GIBSON', location)

    location = re.sub(r'\bCOOPER\b',         'COPPER', location)
    location = re.sub(r'\bCENTAL\b',         'CENTRAL', location)
    location = re.sub(r'\bCURCHILL\b',       'CHURCHILL', location)
    location = re.sub(r'\bCAESAR CHAVEZ\b',  'CESAR CHAVEZ', location)
    location = re.sub(r'\bCONSTITITUON\b',   'CONSTITUTION', location)     
    location = re.sub(r'\bCOMMANCHE\b',      'COMANCHE', location)
    location = re.sub(r'\bLLIFF\b',          'ILIFF', location)
    location = re.sub(r'\b(JUAN TABP|JUAN TABPO|JUAN TAO|JUAN TAB)\b',   'JUAN TABO', location)    
    location = re.sub(r'\b(KATHERINE)\b',   'KATHRYN', location)    
    location = re.sub(r'\b(LOUSIANA|LOUISANA)\b',           'LOUISIANA', location)
    location = re.sub(r'\b(MADIERA|MADERIA)\b',        'MADEIRA', location)
    location = re.sub(r'\b(MALAPAIS)\b',        'MALPAIS', location)
    location = re.sub(r'\b(MLK|MARTIN LUTHER KING)\b',      'DOCTOR MARTIN LUTHER KING JUNIOR', location)
    location = re.sub(r'\b(MARQUETE)\b',        'MARQUETTE', location)
    location = re.sub(r'\b(MENUAL|MANAUL|MANUAL|MANUEL)\b',         'MENAUL', location)
    location = re.sub(r'\bMONTERAY\b',       'MONTEREY', location)
    location = re.sub(r'\b(MOTGOMERY)\b',    'MONTGOMERY', location)                   
    location = re.sub(r'\bROMANW\b',         'ROMA NW', location) 
    location = re.sub(r'\bPLUNKET\b',        'PLUNKETT', location)
    location = re.sub(r'\bPAN AMERICA\b',    'PAN AMERICAN', location)   
    location = re.sub(r'\bPASO DEL\b',       'PASEO DEL', location)
    location = re.sub(r'\bPDN\b',            'PASEO DEL NORTE', location)
    location = re.sub(r'\bPROPECT\b',        'PROSPECT', location)
    location = re.sub(r'\b(PENNSYLVANIEA|PENNAYLVANIA)\b',  'PENNSYLVANIA', location)
    location = re.sub(r'\bSTANDFORD\b',      'STANFORD', location)
    location = re.sub(r'\bSANIDA\b',         'SANDIA', location)
    location = re.sub(r'\bSPANIS\b',         'SPANISH', location)
    location = re.sub(r'\b(SAND PEDRO|SAN PEFRO)\b',     'SAN PEDRO', location)                   
    location = re.sub(r'\b(TRUMBELL|TUMBULL|TRUMBALL|TRUBULL)\b',   'TRUMBULL', location)    
    location = re.sub(r'\b(UNIVERSISTY|UNIVERSIY|UNERSITY)\b',   'UNIVERSITY', location)    

    location = re.sub(r'\bVERDANA\b',        'VERANDA', location)

    location = re.sub(r'\bWESTER SKIES\b',   'WESTERN SKIES', location)
        
    # Insert spaces between digits/characters
    # location = re.sub(r'([0-9]+(\.[0-9]+)?)',r' \1 ', location).strip()
    #location = re.sub(r'([0-9])+(?!RD|ST|ND|TH)',r'\1 ', location).strip()
    
    # Insert between number and letter, except for 1ST, 2ND, etc
    location = re.sub(r'([0-9]+)(?!RD|ST|ND|TH)(?=[A-Z])',r'\1 ', location).strip()
    # Insert between letter and number
    location = re.sub(r'(?<=[A-Z])([0-9]+)',r' \1', location).strip()
    location = re.sub(' +', ' ', location)
    
    # Repair locations with a gap between 1 ST or 2 ND
    # this could be dangerous since ST and RD are common abbreviations
    location = re.sub(r'([0-9]+)\s(ST|ND|RD|TH)\b',r'\1\2', location)
    
    common_address = common_locations(location)
    if common_address:
        return common_address

    # Quadrant Formatting
    location = re.sub(r'\bN/W\b', 'NW', location)
    location = re.sub(r'\bS/W\b', 'SW', location)
    location = re.sub(r'\bN/E\b', 'NE', location)
    location = re.sub(r'\bS/E\b', 'SE', location)

    # Milepost Preformatting
    location = re.sub(r'(\b|\d)(MP|MM|MILE MARKER|MILEMARKER|MILE POST|MILEPOST)(\b|\d)', 'MILEPOST', location)
    location = re.sub(r'\b(NB|SB|EB|WB|E/B|W/B|N/B|S/B|NORTHBOUND|SOUTHBOUND|EASTBOUND|WESTBOUND)\b', '', location)
    location = re.sub(r'\b(NORTH BOUND|SOUTH BOUND|EAST BOUND|WEST BOUND)\b', '', location)
    location = re.sub(r'\b(NORTH OF|SOUTH OF|EAST OF|WEST OF)\b', '', location)  

    # print(location)
    # Highway Preformatting
    location = re.sub(
        r'\b(HIGHWAY|NEW MEXICO HIGHWAY|HWY|NORTH HIGHWAY|N HIGHWAY|STATE RD|IGHWAY|HIGHTWAY|NMHWY|STATE ROAD)\b', 
        'NM', location)
    location = re.sub(r'\b(INTERSTATE 40|1 40|I40|I/40)\b', 'I 40', location)
    location = re.sub(r'\b(INTERSTATE 25|1 25|I25|I/25|1/25)\b', 'I 25', location)
    
    
    # Intersection Preformatting
    # this should be after removal of E/B, 1/25 etc
    location = re.sub(r'\s*/\s*', ' @ ', location)
    location = re.sub(r'\s*&\s*', ' @ ', location)
    location = re.sub(r'\s+AND\s+', ' @ ', location)
    location = re.sub(r'\s+(NEAR|AT|TOWARD|TOWARDS)\s+', ' @ ', location)

    location = re.sub(r'\bFIRST\b',   '1ST', location)
    location = re.sub(r'\bSECOND\b',  '2ND', location)    
    location = re.sub(r'\bTHIRD\b',   '3RD', location)    
    location = re.sub(r'\bFOURTH\b',  '4TH', location)    
    location = re.sub(r'\bFIFTH\b',   '5TH', location)    
    location = re.sub(r'\bSIXTH\b',   '6TH', location)    
    location = re.sub(r'\bSEVENTH\b', '7TH', location)    
    location = re.sub(r'\bEIGHTH\b',  '8TH', location)  
    location = re.sub(r'\bNINTH\b',   '9TH', location)  
    location = re.sub(r'\bTENTH\b',   '10TH', location)  
    
    location = re.sub(r'\bAVW\b',           'AVE', location)    
    location = re.sub(r'\bAVEE\b',          'AVE', location)    
    location = re.sub(r'\bMNE\b',           'NE', location)    
    location = re.sub(r'\bDRIVING\b',       'DR', location)
    location = re.sub(r'\b(BL|BI|BLVE|BLV)\b', 'BLVD', location)
    location = re.sub(r'\bCL\b',            'CIRCLE', location)
    location = re.sub(r'\bLOP\b',           'LOOP', location)  
    location = re.sub(r'\bSST\b',           'ST', location)  

    # remove anything in parentheses
    location = re.sub(r'\([^)]*\)', '', location)
    
    
    rm_phrases = ['WALMART', 'SMITHS', 'PALACE WEST', 'WEST CASINO', 'ISLETA PALACE', 'DILLARDS', 
                 'TARGET', 'HOME DEPOT', 'WALGREENS', 'STARBUCKS', 'PANDA EXPRESS', 'PAPA JOHN', 'KOHLS',
                 'SUBWARY', 'PIZZA HUT', 'BEST BUY', 'LOWES', 'PAPA JOHNS', 'CIRCLE K', 'LOTABURGER', 
                  'AREA OF', 'APPROACHING','LOCATED', 'LARRY H MILLER DEALERSHIP', 'KMART', 'MOTEL 6',
                 '66 GAS STATION', 'GAS STATION', 'SPEEDWAY', 'DK', 'GIANT', 'FLL UP', 'PHILLIPS',                  
                 'VALERO', 'MAVERIK', 'MAVERICK', 'SHELL', 'PIT STOP', '7/11','CHEVRON', 'LOVES', 
                 'ISLETA TRAVEL CENTER', 'UNDER GROUND', 'ARROYO', 'ALLEY', 'IN', 'THE', 'AREA',
                  'ON', 'BLOCK OF', 'ALBERTSONS', 'INTERSECTION', 'THE', 'AT', 'NEAR', 'OF', 'CORNER',
                 'PARKING LOT', 'SOUTH LOT', 'DIRT LOT',  'FOR', 'BOSQUE', 'PARKING','STRUCTURE']
    
    rm_str = fr'\b' + fr'\b|\b'.join(rm_phrases) + fr'\b'
    location = re.sub(rm_str, '', location)

    # Remove apartment/unit Numbers
    location = re.sub(r'\b(APARTMENT|APT|UNIT|BLDG|SUITE).+', '', location)
    
    if 'MILEPOST' in location:
        location = sanitize_milepost(location)
    else:     
        # Remove everything after #
        location = re.sub(r'#.+', '', location)

    # Remove extra @, commas, etc
    location = re.sub(r'^(@|,|;)', '', location.strip())
    location = re.sub(r'(@|,|;)$', '', location.strip())
    location = re.sub(' +', ' ', location)
    location = location.strip()

    return location

def sanitize_milepost(location):
    # remove NORTH, SOUTH, etc
    rm_phrases = ['NORTH', 'SOUTH', 'EAST', 'WEST','N', 'S', 'E', 'W']
    rm_str = fr'\b' + fr'\b|\b'.join(rm_phrases) + fr'\b'
    location = re.sub(rm_str, '', location)
    location = re.sub(r'^(@|,|;)', '', location.strip())
    location = re.sub(r'(@|,|;)$', '', location.strip())
    location = re.sub(r'#', '', location)
    location = re.sub(' +', ' ', location.strip())
    
    # sometimes NM 14, sometimes 14 NM
    #location = re.sub(r'([0-9]+) NM',r'NM \1', location)
    location = re.sub(r'^125|^25\b',r'I 25', location)
    location = re.sub(r'^140|^40\b',r'I 40', location)
    location = re.sub(r'^47\b',r'NM 47', location)
    location = re.sub(r'^333\b',r'NM 333', location)
    
    location = re.sub(r'(SANDIA CREST|SANDIA CREST RD|CREST RD|CREST ROAD|CREST)', 'NM 47', location)
    location = re.sub(r'(PASEO DEL NORTE|PASEO|PASEODEL NORTE)', 'NM 423', location)
    location = re.sub(r'(TRAMWAY|TRAMWAY BLVD|TRAMWAY RD)', 'NM 556', location)

    
    # NM 40 does not exist, must be I 40
    location = re.sub(r'\bNM 40\b',r'I 40', location)
    # NM 25 does not exist, must be I 25
    location = re.sub(r'\bNM 25\b',r'I 25', location)

    #print(location)
    mp = re.findall(r'MILEPOST (\d+)', location)
    if not mp:
        mp = re.findall(r'(\d+) MILEPOST', location)
    if not mp:
        mp = re.findall(r'(?<!M|I) (\d+)\b', location)
        
    rte_prefix_num = re.findall(r'\b(I|NM|US) (\d+)\b', location)
    if not rte_prefix_num:
        location = re.sub(r'\b(\d+) (I|NM|US)\b',r'\2 \1', location)
        rte_prefix_num = re.findall(r'\b(I|NM|US) (\d+)\b', location)        
    
    if mp and rte_prefix_num:
        location = f'{rte_prefix_num[0][0]} {rte_prefix_num[0][1]} @ MILEPOST {mp[0]}'
    
    return location
    
    
def common_locations(location):
    location_out = ''
    if bool(re.search(r'\b(SANDIA RESORT|SANDIA CASINO|30 RAINBOW)\b', location)):
        location_out = '30 RAINBOW RD, ALBUQUERQUE, NM 87151'
    elif bool(re.search(r'\b(ISLETA TRAVEL)\b', location)):
        location_out = '4050 NM 47, ALBUQUERQUE, NM 87105'
    elif bool(re.search(r'\b(ISLETA PALACE|PALACE WEST)\b', location)):
        location_out = '2 NM 45, ALBUQUERQUE, NM 87105'
    elif bool(re.search(r'\b(MDC|METROPOLITAN DETENTION CENTER|100 DEPUTY|100 DEAN|100 JOHN DANTIS|100 JOHN DANTES|100 DUPUTY DEAN)\b', location)):
        location_out = '100 DEPTUY DEAN MIERA DR SW, ALBUQUERQUE, NM 87151'
    elif bool(re.search(r'\b(ISLETA CASINO|ISLETA RESORT)\b', location)):
        location_out = '11000 BROADWAY BLVD SE, ALBUQUERQUE, NM 87105'
    elif bool(re.search(r'\b(UNMH|UNM Hospital)\b', location)):
        location_out = '2211 LOMAS BLVD NE, ALBUQUERQUE, NM 87106'
    elif bool(re.search(r'\b(STATE FAIGROUNDS|SATE FAIR|STATE FAIRGROUNDS)\b', location)):
        location_out = '300 SAN PEDRO DR NE, ALBUQUERQUE, NM 87108'
    elif bool(re.search(r'\b(THE DOWNS|DOWNS CASINO)\b', location)):
        location_out = 'LOUISIANA BLVD NE, ALBUQUERQUE, NM 87108'

    return location_out


def geocode_intersection(location, df_intersection):

    gc = geocode_default()
    gc['gc_geocoder']  = 'intersection'
    #return gc

    if location == '':
        return gc
            
    df_match = df_intersection[df_intersection.roads_stripped.map(lambda x: intersection_match(x, location)) > 1 ].copy()
    #print(df_match)
    
    if len(df_match)<1:
        return gc
    else:
        df_match = df_match.sort_values(by = 'n_stripped', ascending = True, na_position = 'last')
        # sort so that intersections with the minimal number of roads is first
        df_match = df_match.iloc[0]
        # print(df_match)
        
        gc['gc_street_address'] = ' @ '.join(df_match.roads).upper() #location
        gc['gc_city']           = ''
        gc['gc_state']          = 'NM'
        gc['gc_zip_code']       = ''
        gc['gc_lat']            = df_match.x_lat
        gc['gc_lon']            = df_match.x_lon
        gc['gc_confidence']     = 1.0
    return gc 

def intersection_match(road_list, location):
    n_match = 0
    for r in road_list: 
        n_match = n_match + bool(re.search(fr'\b{r}\b', location))
        # if n_match > 1:
        #     return n_match
    return n_match


def geocode_milepost(clean_location, df_milepost):
    gc = geocode_default()
    gc['gc_geocoder'] = 'milepost'
    mp = re.findall(r'MILEPOST (\d+)', clean_location)
    rte_prefix_num = re.findall(r'\b(I|NM|US) (\d+)\b', clean_location)
    
    if mp and rte_prefix_num:
        df_match = df_milepost[(df_milepost.routeprefix == rte_prefix_num[0][0]) &
                    (df_milepost.routenumber == rte_prefix_num[0][1]) &
                    (df_milepost.milepost == mp[0])
                   ]
        if len(df_match)<1:
            return gc
        else:
            df_match = df_match.iloc[0]
            gc['gc_street_address'] = f'{rte_prefix_num[0][0]} {rte_prefix_num[0][1]} @ MILEPOST {mp[0]}'
            gc['gc_city']           = ''
            gc['gc_state']          = 'NM'
            gc['gc_zip_code']       = ''
            gc['gc_lat']            = df_match.latitude
            gc['gc_lon']            = df_match.longitude
            gc['gc_confidence']     = 1.0
            return gc
    else:
        return gc
    
    