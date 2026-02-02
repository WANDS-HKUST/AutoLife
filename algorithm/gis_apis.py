#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/1/2024
# @Author  : Huatao
# @Email   : 735820057@qq.com
# @File    : gis_apis.py
# @Description :

import requests


def get_location_name(latitude, longitude, api_key):
    """
    Get the location name using Google Maps Geocoding API.

    Parameters:
    - latitude (float): Latitude of the location.
    - longitude (float): Longitude of the location.
    - api_key (str): API key for Google Maps.

    Returns:
    - str: The name of the location.
    """
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "latlng": f"{latitude},{longitude}",
        "key": api_key
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        results = response.json()['results']
        if results:
            # Return the formatted address of the first result
            return results[0]['formatted_address']
        else:
            return "No location found"
    else:
        return "Error: Unable to connect to the API"


def get_point_of_interest_new(latitude, longitude, api_key):
    """
    Get the location name using Google Maps Geocoding API.

    Parameters:
    - latitude (float): Latitude of the location.
    - longitude (float): Longitude of the location.
    - api_key (str): API key for Google Maps.

    Returns:
    - str: The name of the location.
    """
    base_url = "https://places.googleapis.com/v1/places:searchNearby"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.displayName"
    }

    params = {
        "maxResultCount": 20,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "radius": 500
            }
        },
        "languageCode": "en"
    }

    response = requests.post(base_url, headers=headers, json=params)

    if response.status_code == 200:
        results = response.json()
        if results:
            # Return the formatted address of the first result
            return results[0]['formatted_address']
        else:
            return "No location found"
    else:
        return "Error: Unable to connect to the API"

def get_google_map_image(latitude, longitude, api_key, zoom=18, size='500x500', maptype='roadmap', language='en',
                         save_path=None, marker=False):
    """
    Fetches a map image from Google Static Maps API.

    Parameters:
    - longitude (float): The longitude of the center of the map.
    - latitude (float): The latitude of the center of the map.
    - api_key (str): Your Google Maps API key.
    - zoom (int): The zoom level of the map.
    - size (str): The size of the map in pixels, formatted activity_sensing {width}x{height}.
    - maptype (str): The type of map to construct. Options are 'roadmap', 'satellite', 'hybrid', 'terrain'.
    - marker (bool): If True, place a red marker at the center of the map.

    Returns:
    - bytes: The image data in bytes. None if request fails.
    """
    base_url = "https://maps.googleapis.com/maps/api/staticmap?"

    # Adding marker parameters if marker is True
    markers_param = f"color:red|{latitude},{longitude}" if marker else ""

    params = {
        "center": f"{latitude},{longitude}",
        "zoom": zoom,
        "size": size,
        "maptype": maptype,
        "key": api_key,
        "language": language,
        "markers": markers_param  # Add this only if there are markers to display
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        if save_path is not None:
            with open(save_path, "wb") as file:
                file.write(response.content)
                print(f"Fetch the map image at {save_path}")
            return response.content
        else:
            return response.content
    else:
        print(f"Failed to fetch the map image. Status code: {response.status_code}")
        return None


def get_google_map_image_markers(coords, api_key, zoom=19, size='500x500', maptype='roadmap', language='en',
                                 save_path=None):
    """
    Fetches a static Google Map image with markers for the given coordinates.

    Parameters:
    - coords: List of tuples, where each tuple contains (longitude, latitude).
    - api_key: String, your Google API key.
    - zoom: Integer, zoom level of the map.
    - size: String, size of the map image in format 'widthxheight'.
    - maptype: String, type of map. Options are 'roadmap', 'satellite', 'hybrid', 'terrain'.
    - language: String, language used for map labels.

    Returns:
    - A requests.Response object containing the map image or error.
    """
    # Base URL for the Google Maps Static API
    base_url = "https://maps.googleapis.com/maps/api/staticmap?"

    # Constructing the markers parameter
    markers_params = '|'.join(f"color:red%7Clabel:{idx + 1}%7C{lat},{lon}" for idx, (lon, lat) in enumerate(coords))

    # Constructing the full URL
    map_url = f"{base_url}size={size}&maptype={maptype}&language={language}&zoom={zoom}&markers={markers_params}&key={api_key}"

    # Making the request to get the map image
    response = requests.get(map_url)

    if response.status_code == 200:
        if save_path is not None:
            with open(save_path, "wb") as file:
                file.write(response.content)
        return response.content
    else:
        print(f"Failed to fetch the map image. Status code: {response.status_code}")
        return None


def get_amap_image(latitude, longitude, api_key, zoom=17, size='500*500', scale=1, maptype='roadmap',
                   save_path=None):
    # Construct the Amap API URL
    url = f'https://restapi.amap.com/v3/staticmap'

    # Set the parameters for the API request
    params = {
        'location': f'{longitude},{latitude}',  # Longitude, Latitude
        'zoom': zoom,  # Zoom level
        'size': size,  # Image size
        'scale': scale,  # Image scale (1 for standard, 2 for high-definition)
        'key': api_key  # Your Amap API Key
    }

    # Send the request and get the response
    response = requests.get(url, params=params)

    if response.status_code == 200:
        # If the request is successful, save the map image
        if save_path is not None:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f'Map image saved to {save_path}')
        return response.content
    else:
        print('Error: Failed to get map image')
        return None


if __name__ == "__main__":
    api_key = "YOUR_KEY"
    api_key_amap = "YOUR KEY"

    latitude, longitude = 22.529828, 114.052065

    #
    map_image = get_google_map_image(latitude, longitude, api_key, save_path="test_google.png")
    map_image_amap = get_amap_image(latitude, longitude, api_key_amap, save_path="test_amap.png")

