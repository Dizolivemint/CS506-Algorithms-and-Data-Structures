from dotenv import load_dotenv
import os
import requests
import pandas as pd

def get_distance_matrix(api_key, origins, destinations):
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
    df = pd.DataFrame(distance_matrix, index=origins, columns=origins)
    df.to_csv(filename)
    print(f"Distance matrix saved to {filename}")

def main():
    load_dotenv()
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    
    if api_key is None:
        raise ValueError("API key not found")
      
    cities = [
        "New York City, NY",
        "Sacramento, CA",
        "Chicago, IL",
        "Austin, TX",
        "Tucson, AZ",
        "Philadelphia, PA",
        "San Antonio, TX",
        "San Diego, CA",
        "Dallas, TX",
        "San Francisco, CA"
    ]
    
    response = get_distance_matrix(api_key, cities, cities)
    distance_matrix = parse_distance_matrix(response)
    save_to_csv(distance_matrix, cities)

if __name__ == "__main__":
    main()