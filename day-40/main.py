import time
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

ORIGIN_CITY_IATA = "LON"

for row in sheet_data:
    if not row["iataCode"]: 
        city_name = row["city"]
        try:
            iata_code = flight_search.get_destination_code(city_name)
            row["iataCode"] = iata_code
            logger.info(f"IATA code updated for {city_name}: {iata_code}")
        except Exception as e:
            logger.error(f"Error updating IATA code for {city_name}: {e}")
        time.sleep(2) 

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()


customer_data = data_manager.get_customer_emails()
customer_email_list = [row.get("whatIsYourEmail?") for row in customer_data if row.get("whatIsYourEmail?")]
logger.info(f"Retrieved {len(customer_email_list)} customer emails")


tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    logger.info(f"Getting flights for {destination['city']}...")
    try:
        flights = flight_search.check_flights(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=tomorrow,
            to_time=six_month_from_today
        )
        cheapest_flight = find_cheapest_flight(flights)

        logger.info(f"Cheapest direct flight to {destination['city']}: £{cheapest_flight.price}")
        
        if cheapest_flight.price == "N/A":
            logger.info(f"No direct flight found for {destination['city']}. Searching for indirect flights...")
            stopover_flights = flight_search.check_flights(
                ORIGIN_CITY_IATA,
                destination["iataCode"],
                from_time=tomorrow,
                to_time=six_month_from_today,
                is_direct=False
            )
            cheapest_flight = find_cheapest_flight(stopover_flights)
            logger.info(f"Cheapest indirect flight to {destination['city']}: £{cheapest_flight.price}")

        if cheapest_flight.price != "N/A" and cheapest_flight.price < destination.get("lowestPrice", float('inf')):
            if cheapest_flight.stops == 0:
                message = f"Low price alert! Only GBP {cheapest_flight.price} to fly direct "\
                          f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "\
                          f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
            else:
                message = f"Low price alert! Only GBP {cheapest_flight.price} to fly "\
                          f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "\
                          f"with {cheapest_flight.stops} stop(s) "\
                          f"departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}."

            logger.info(f"Sending notifications for {destination['city']}")
            notification_manager.send_whatsapp(message_body=message)
            notification_manager.send_emails(email_list=customer_email_list, email_body=message)

    except Exception as e:
        logger.error(f"Error processing flights for {destination['city']}: {e}")

    time.sleep(2) 
