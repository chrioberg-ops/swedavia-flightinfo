# Swedavia FlightInfo Client

A Python application that retrieves real-time flight information from the Swedavia FlightInfo API.

## Features

- View arriving flights
- View departing flights
- Search for a flight number
- Display terminal information
- Display flight status
- Airport lookup using JSON configuration
- Filters out cancelled/deleted flights

## Technologies Used

- Python 3
- Requests
- REST API
- JSON
- Git & GitHub

## Installation

Clone the repository:

```bash
git clone https://github.com/chrioberg-ops/swedavia-flightinfo.git
cd swedavia-flightinfo
```

Install dependencies:

```bash
pip install requests
```

Set your API key:

```bash
export SWEDAVIA_API_KEY="YOUR_API_KEY"
```

Run the application:

```bash
python3 swedavia_flightinfo.py
```

## Example Output

```text
Flight: D84323
Airline: Norwegian
From: Stockholm Arlanda Airport
To: Nice
Status: Planerad / Scheduled
```

## Project Goal

The goal of this project was to reverse engineer an existing application using the Swedavia FlightInfo API and recreate the functionality in Python.

During development I analyzed the API structure, handled JSON responses, implemented flight filtering, and improved the user experience by displaying only active flights.

## Skills Demonstrated

- API Integration
- Python Development
- JSON Processing
- Troubleshooting
- Reverse Engineering
- Git Version Control
- Command Line Usage
