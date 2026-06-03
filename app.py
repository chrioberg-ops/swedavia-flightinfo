import os
import json
import requests
from datetime import date
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = os.getenv("SWEDAVIA_API_KEY")
BASE_URL = "https://api.swedavia.se/flightinfo/v2"

HEADERS = {
    "Accept": "application/json",
    "Ocp-Apim-Subscription-Key": API_KEY
}


def load_airports():
    with open("airports.json", "r", encoding="utf-8") as file:
        return json.load(file)


def get_flights(airport, flight_type, flight_date):
    url = f"{BASE_URL}/{airport}/{flight_type}/{flight_date}"

    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()

    data = response.json()
    return data.get("flights", [])


def get_nested(data, *keys, default="N/A"):
    current = data

    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key)

    if current is None or current == "":
        return default

    return current


def get_time(flight, time_type):
    time_data = flight.get(time_type)

    if isinstance(time_data, dict):
        return (
            time_data.get("scheduledUtc")
            or time_data.get("estimatedUtc")
            or time_data.get("actualUtc")
            or time_data.get("scheduledLocal")
            or time_data.get("estimatedLocal")
            or time_data.get("actualLocal")
            or "N/A"
        )

    if isinstance(time_data, str) and time_data.strip():
        return time_data

    return "N/A"


def filter_flights(flights, flight_number):
    filtered = []

    for flight in flights:
        status = get_nested(flight, "locationAndStatus", "flightLegStatus", default="")

        if status == "DEL":
            continue

        flight_id = str(flight.get("flightId", ""))

        if flight_number:
            if flight_number.lower() not in flight_id.lower():
                continue

        filtered.append(flight)

    return filtered[:30]


def simplify_flight(flight, selected_airport_name, flight_type):
    flight_id = flight.get("flightId", "N/A")
    airline = get_nested(flight, "airlineOperator", "name")

    departure_airport = (
        flight.get("departureAirportEnglish")
        or flight.get("departureAirportSwedish")
        or "N/A"
    )

    arrival_airport = (
        flight.get("arrivalAirportEnglish")
        or flight.get("arrivalAirportSwedish")
        or "N/A"
    )

    if flight_type == "arrivals":
        from_place = departure_airport
        to_place = selected_airport_name
    else:
        from_place = selected_airport_name
        to_place = arrival_airport

    scheduled_time = (
        get_time(flight, "arrivalTime")
        if flight_type == "arrivals"
        else get_time(flight, "departureTime")
    )

    return {
        "flight_id": flight_id,
        "airline": airline,
        "from": from_place,
        "to": to_place,
        "scheduled_time": scheduled_time,
        "terminal": get_nested(flight, "locationAndStatus", "terminal"),
        "gate": get_nested(flight, "locationAndStatus", "gate"),
        "status": (
            get_nested(flight, "locationAndStatus", "flightLegStatusSwedish")
            + " / "
            + get_nested(flight, "locationAndStatus", "flightLegStatusEnglish")
        )
    }


@app.route("/", methods=["GET", "POST"])
def index():
    airports = load_airports()
    today = date.today().isoformat()

    selected_airport = "ARN"
    selected_type = "arrivals"
    selected_date = today
    flight_number = ""

    results = []
    error = None
    search_done = False

    if request.method == "POST":
        search_done = True

        selected_airport = request.form.get("airport", "ARN").upper().strip()
        selected_type = request.form.get("flight_type", "arrivals").strip()
        selected_date = request.form.get("date") or today
        flight_number = request.form.get("flight_number", "").strip()

        if not API_KEY:
            error = "API-nyckel saknas på servern. Sätt SWEDAVIA_API_KEY innan appen startas."
        elif selected_airport not in airports:
            error = "Ogiltig flygplatskod."
        elif selected_type not in ["arrivals", "departures"]:
            error = "Ogiltig söktyp."
        else:
            try:
                selected_airport_name = airports.get(selected_airport, selected_airport)
                flights = get_flights(selected_airport, selected_type, selected_date)
                filtered_flights = filter_flights(flights, flight_number)

                results = [
                    simplify_flight(flight, selected_airport_name, selected_type)
                    for flight in filtered_flights
                ]

            except requests.exceptions.HTTPError as e:
                error = f"API-fel: {e}"
            except requests.exceptions.RequestException as e:
                error = f"Kunde inte kontakta Swedavia API: {e}"
            except Exception as e:
                error = f"Något gick fel: {e}"

    return render_template(
        "index.html",
        airports=airports,
        today=today,
        selected_airport=selected_airport,
        selected_type=selected_type,
        selected_date=selected_date,
        flight_number=flight_number,
        results=results,
        error=error,
        search_done=search_done
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
