from math import isnan
import json
from numpy import nan


def dict_clean(d):
    result = {}
    for key, value in d.items():
        if value == nan:
            value = 'test'
        result[key] = value
    print(result)
    return result

def deleteNone(d):

    #Delete keys with the value ``None`` in a dictionary, recursively.
    
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            deleteNone(value)
    return d 


def traverseLocation(x,loc):
    if(x in loc):
        return(loc[x])
    

def axisDetailedAddress(location):
    address={
        'village'           : (traverseLocation('village',location)),
        'area'              : (traverseLocation('place_name',location)),
        'suburb'            : (traverseLocation('suburb',location)),
        'tehsil'            : (traverseLocation('county',location)),
        'district'          : (traverseLocation('county_name',location)),
        'city'              : (traverseLocation('city',location)),
        'city_District'     : (traverseLocation('city_district',location)),
        'state_district'    : (traverseLocation('state_district',location)),
        'state'             : (traverseLocation('state',location)),
        'country'           : (traverseLocation('country',location)),
        'postal_Code'       : (traverseLocation('postal_code',location)),
        'postalCode'       : (traverseLocation('postcode',location))

    }

    return (json.loads((json.dumps(address).replace("NaN" ,  "0",))))

def pincodeDetailedAddress(location):
  

    address = {
        'area': location['place_name'],
        'tehsil': location['community_name'],
        'district':location['county_name'],
        'state':location['state_name'],
        'country_code':location['country_code'],
        'latitude':location['latitude'],
        'longitude':location['longitude']

    }
    #print(json.loads((json.dumps(address).replace("NaN" ,  "0",))))
    return (json.loads((json.dumps(address).replace("NaN" ,  "0",))))