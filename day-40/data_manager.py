import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

class DataManager:
    def __init__(self):
        load_dotenv()
        self._user = os.getenv("SHEETY_USERNAME")
        self._password = os.getenv("SHEETY_PASSWORD")
        self.prices_endpoint = os.getenv("SHEETY_PRICES_ENDPOINT")
        self.users_endpoint = os.getenv("SHEETY_USERS_ENDPOINT")
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.destination_data = {}
        self.customer_data = {}

    def _get_data_from_sheet(self, endpoint):
        try:
            response = requests.get(url=endpoint, auth=self._authorization)
            response.raise_for_status() 
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {endpoint}: {e}")
            return None

    def get_destination_data(self):
        data = self._get_data_from_sheet(self.prices_endpoint)
        if data:
            self.destination_data = data.get("prices", [])
        return self.destination_data

    def get_customer_emails(self):
        data = self._get_data_from_sheet(self.users_endpoint)
        if data:
            self.customer_data = data.get("users", [])
        return self.customer_data

    def update_destination_codes(self):
        if not self.destination_data:
            self.get_destination_data()

        for city in self.destination_data:
            new_data = {"price": {"iataCode": city.get("iataCode")}}
            try:
                response = requests.put(
                    url=f"{self.prices_endpoint}/{city['id']}",
                    json=new_data,
                    auth=self._authorization
                )
                response.raise_for_status()
                print(f"Update successful for {city['id']}")
            except requests.exceptions.RequestException as e:
                print(f"Error updating data for {city['id']}: {e}")
