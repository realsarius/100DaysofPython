class FlightData:

    def __init__(self, price, origin_airport, destination_airport, out_date, return_date, stops):

        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops

def find_cheapest_flight(data):


    try:
        if not data or not data.get('data'):
            print("No flight data")
            return FlightData(
                price="N/A",
                origin_airport="N/A",
                destination_airport="N/A",
                out_date="N/A",
                return_date="N/A",
                stops="N/A"
            )

        cheapest_flight = None
        lowest_price = float('inf')

        for flight in data["data"]:
            price = float(flight["price"]["grandTotal"])

            if price < lowest_price:
                lowest_price = price
                segments = flight["itineraries"][0]["segments"]
                nr_stops = len(segments) - 1 

                origin = segments[0]["departure"]["iataCode"]
                destination = segments[nr_stops]["arrival"]["iataCode"]

                out_date = segments[0]["departure"]["at"].split("T")[0]
                return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

                cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date, nr_stops)
                print(f"Lowest price to {destination} is £{lowest_price}")

        return cheapest_flight if cheapest_flight else FlightData(
            price="N/A",
            origin_airport="N/A",
            destination_airport="N/A",
            out_date="N/A",
            return_date="N/A",
            stops="N/A"
        )

    except KeyError as e:
        print(f"Error parsing data: {e}")
        return FlightData(
            price="N/A",
            origin_airport="N/A",
            destination_airport="N/A",
            out_date="N/A",
            return_date="N/A",
            stops="N/A"
        )