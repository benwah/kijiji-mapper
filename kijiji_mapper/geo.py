import requests
from kijiji_mapper import settings


def geolocate(address, settigns):
    payload = {
        "address": address,
        "key": API_KEY,
    }

    result = requests.get(GOOGLE_MAPS_URL, params=payload)

    result_object = result.json()
    result_results = result_object["results"]
    if len(result_results) < 1:
        return None

    result_geometry = result_results[0]["geometry"]
    latlong = result_geometry["location"]

    return [latlong['lat'], latlong['lng']]
