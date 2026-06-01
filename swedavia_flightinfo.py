import os
import json
import requests
from datetime import date

API_KEY = os.getenv("SWEDAVIA_API_KEY")
BASE_URL = "https://api.swedavia.se/flightinfo/v2"

with open("airports.json", "r", encoding="utf-8") as f:
    AIRPORT_NAMES = json.load(f)

HEADERS = {
    "Accept": "application/json",
    "Ocp-Apim-Subscription-Key": API_KEY
}


def get_flights(airport, flight_type, flight_date):
    url = f"{BASE_URL}/{airport}/{flight_type}/{flight_date}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
    except requests.exceptions.RequestException as error:
        print("Kunde inte ansluta till API:")
        print(error)
        return []

    if response.status_code != 200:
        print("API error:", response.status_code)
        print(response.text)
        return []

    data = response.json()
    return data.get("flights", [])


def print_flights(flights, airport, flight_type):
    if not flights:
        print("Inga flyg hittades.")
        return

    selected_airport = AIRPORT_NAMES.get(airport.upper(), airport.upper())

    active_flights = [
        flight for flight in flights
        if flight.get("locationAndStatus", {}).get("flightLegStatus") != "DEL"
    ]

    if not active_flights:
        print("Inga aktiva flyg hittades.")
        return

    for flight in active_flights[:20]:
        flight_id = flight.get("flightId", "Okänt")
        airline = flight.get("airlineOperator", {}).get("name", "Okänt")

        location = flight.get("locationAndStatus", {})
        terminal = location.get("terminal", "Okänd")
        status_sv = location.get("flightLegStatusSwedish", "Okänd")
        status_en = location.get("flightLegStatusEnglish", "Okänd")

        arrival_time = flight.get("arrivalTime", {}).get("scheduledUtc", "")
        departure_time = flight.get("departureTime", {}).get("scheduledUtc", "")

        departure = flight.get("departureAirportEnglish") or flight.get("departureAirportSwedish") or "Okänt"
        arrival = flight.get("arrivalAirportEnglish") or flight.get("arrivalAirportSwedish") or "Okänt"

        if flight_type == "arrivals":
            from_place = departure
            to_place = selected_airport
        else:
            from_place = selected_airport
            to_place = arrival

        print("-" * 50)
        print(f"Flight:        {flight_id}")
        print(f"Airline:       {airline}")
        print(f"From:          {from_place}")
        print(f"To:            {to_place}")
        print(f"Departure UTC: {departure_time}")
        print(f"Arrival UTC:   {arrival_time}")
        print(f"Terminal:      {terminal}")
        print(f"Status:        {status_sv} / {status_en}")


def search_flight(flights, flight_number):
    results = []

    for flight in flights:
        flight_id = str(flight.get("flightId", ""))
        if flight_number.lower() in flight_id.lower():
            results.append(flight)

    return results


def main():
    if not API_KEY:
        print("Du måste sätta API-nyckeln först:")
        print('export SWEDAVIA_API_KEY="DIN_NYCKEL"')
        return

    while True:
        print("\n=== Swedavia FlightInfo API ===")
        print("1. Visa arrivals")
        print("2. Visa departures")
        print("3. Sök flightnummer")
        print("4. Avsluta")

        choice = input("Välj: ")

        if choice == "4":
            print("Avslutar programmet.")
            break

        airport = input("Airport IATA, t.ex ARN, BMA, GOT, MMX: ").upper()
        flight_date = input(f"Datum YYYY-MM-DD, enter för idag ({date.today()}): ")

        if flight_date == "":
            flight_date = str(date.today())

        if choice == "1":
            flight_type = "arrivals"
            flights = get_flights(airport, flight_type, flight_date)
            print_flights(flights, airport, flight_type)

        elif choice == "2":
            flight_type = "departures"
            flights = get_flights(airport, flight_type, flight_date)
            print_flights(flights, airport, flight_type)

        elif choice == "3":
            flight_type = input("arrivals eller departures: ").lower()
            flight_number = input("Flightnummer, t.ex SK1427: ")

            flights = get_flights(airport, flight_type, flight_date)
            results = search_flight(flights, flight_number)
            print_flights(results, airport, flight_type)

        else:
            print("Fel val. Välj 1, 2, 3 eller 4.")


if __name__ == "__main__":
    main()