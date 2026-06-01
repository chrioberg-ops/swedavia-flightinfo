# Swedavia FlightInfo Client

A Python application that retrieves flight information from the Swedavia FlightInfo API.

## Features

* View arriving flights
* View departing flights
* Search for a flight number
* Display terminal information
* Display flight status
* Airport lookup using JSON configuration
* Filters out cancelled/deleted flights

## Technologies Used

* Python 3
* Requests
* REST API
* JSON
* Git & GitHub

## Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/swedavia-flightinfo.git

Install dependencies:

pip install requests

Set your API key:

export SWEDAVIA_API_KEY="YOUR_API_KEY"

Run the application:

python3 swedavia_flightinfo.py

## Example Output

Flight: D84323
Airline: Norwegian
From: Stockholm Arlanda Airport
To: Nice
Status: Planerad / Scheduled

## Project Goal

The goal of this project was to reverse engineer an existing application using the Swedavia FlightInfo API and recreate the functionality in Python while improving usability and maintainability.

---

### 3. Lägg upp på GitHub

I terminalen:

```bash
cd ~/swedavia_flightinfo

git init
git add .
git commit -m "Initial commit"

git branch -M main