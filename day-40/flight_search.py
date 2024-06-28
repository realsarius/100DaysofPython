import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"

class FlightSearch:

    def __init__(self):

        self._api_key = os.getenv("AMADEUS_API_KEY")
        self._api_secret = os.getenv("AMADEUS_SECRET")
        self._token = None
        self._token_expiry = None
        self._get_or_refresh_token()

    def _get_or_refresh_token(self):

        if not self._token or (self._token_expiry and datetime.now() >= self._token_expiry):
            self._token = self._get_new_token()
            self._token_expiry = datetime.now() + timedelta(seconds=1799)

    def _get_new_token(self):

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }
        response = requests.post(url=TOKEN_ENDPOINT, headers=headers, data=body)

        if response.status_code != 200:
            raise RuntimeError(f"Failed to obtain token: {response.status_code} - {response.text}")

        access_token = response.json().get('access_token')
        expires_in = response.json().get('expires_in', 0)
        print(f"New token obtained. Expires in {expires_in} seconds.")
        return access_token

    def get_destination_code(self, city_name):
        
        self._get_or_refresh_token()

        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "keyword": city_name,
            "max": "1",
            "subType": "CITY"
        }
        response = requests.get(
            url=IATA_ENDPOINT,
            headers=headers,
            params=query
        )

        if response.status_code != 200:
            print(f"Failed to retrieve IATA code for {city_name}: {response.status_code} - {response.text}")
            return "N/A"

        try:
            code = response.json()["data"][0]['iataCode']
        except IndexError:
            print(f"No airport code found for {city_name}.")
            return "N/A"
        except KeyError:
            print(f"No airport code found for {city_name}.")
            return "Not Found"

        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time, is_direct=True):

        self._get_or_refresh_token()

        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true" if is_direct else "false",
            "currencyCode": "GBP",
            "max": "10",
        }

        response = requests.get(
            url=FLIGHT_ENDPOINT,
            headers=headers,
            params=query,
        )

        if response.status_code != 200:
            print(f"Failed to retrieve flight offers: {response.status_code} - {response.text}")
            print("For details on status codes, check the API documentation:")
            print("https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api-reference")
            return None

        return response.json()
