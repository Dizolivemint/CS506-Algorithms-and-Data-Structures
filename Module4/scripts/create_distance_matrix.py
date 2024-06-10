from dotenv import load_dotenv
import os
import requests
import pandas as pd
from cities import cities_generator

def get_distance_matrix(api_key, origins, destinations):
    """
    Fetches the distance matrix from the Google Maps Distance Matrix API.

    Parameters:
    api_key (str): The API key for accessing the Google Maps API.
    origins (list): A list of origin city names.
    destinations (list): A list of destination city names.

    Returns:
    dict: The JSON response from the Google Maps API.
    """
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    origins_str = "|".join(origins)
    destinations_str = "|".join(destinations)
    params = {
        "origins": origins_str,
        "destinations": destinations_str,
        "units": "imperial",
        "key": api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def parse_distance_matrix(response):
    """
    Parses the distance matrix from the API response.

    Parameters:
    response (dict): The JSON response from the Google Maps API.

    Returns:
    list: A 2D list representing the distance matrix.
    """
    rows = response['rows']
    distance_matrix = []
    for row in rows:
        distances = []
        for element in row['elements']:
            distance = element['distance']['value']  # distance in meters
            distances.append(distance)
        distance_matrix.append(distances)
    return distance_matrix

def save_to_csv(distance_matrix, origins, filename="distance_matrix.csv"):
    """
    Saves the distance matrix to a CSV file.

    Parameters:
    distance_matrix (list): The 2D list representing the distance matrix.
    origins (list): A list of city names.
    filename (str): The name of the CSV file to save the distance matrix.
    """
    # Ensure the filename is unique
    i = 0
    while os.path.exists(filename):
        filename = f"distance_matrix_{i}.csv"
        i += 1
    df = pd.DataFrame(distance_matrix, index=origins, columns=origins)
    df.to_csv("data/" + filename)
    print(f"Distance matrix saved to {filename}")

def main():
    """
    Main function to generate and save the distance matrix.
    """
    load_dotenv()
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    
    if api_key is None:
        raise ValueError("API key not found")
      
    # Get 10 random cities from cities
    cities = cities_generator.get_cities(10)
    
    response = get_distance_matrix(api_key, cities, cities)
    distance_matrix = parse_distance_matrix(response)
    save_to_csv(distance_matrix, cities)

if __name__ == "__main__":
    main()