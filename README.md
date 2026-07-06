# BachelorNest 🏠

**A bachelor-friendly rental finder that connects home-seekers directly with property owners — no brokers, no hidden contacts.**

## About

Finding rental accommodation as a student or young working bachelor in Indian cities is harder than it should be. BachelorNest solves this with a lightweight, locally-run web app built specifically around bachelor needs.

## Features

- Secure sign-in and multi-role sign-up
- Dynamic multi-parameter rental dashboard with sidebar filters
- Property detail views with owner profiles
- WhatsApp integration for direct owner contact
- Save and track favorite listings
- Landlord property posting form

## Tech Stack

- Frontend: Streamlit, custom CSS
- Backend: Python 3
- Storage: Flat-file JSON

## Project Structure
streamlit-house-app/
├── .streamlit/config.toml
├── data/
│   ├── listings.json
│   └── users.json
├── backend/
│   ├── database.py
│   └── validators.py
├── frontend/
│   ├── styles.py
│   ├── auth_views.py
│   └── dashboards.py
└── main.py

## Setup & Installation

```bash
git clone https://github.com/NakshatraReddy001/bachelornest.git
cd bachelornest
pip install -r requirements.txt
streamlit run main.py
```

## Future Enhancements

- Migrate from flat-file JSON to a cloud-hosted database
- Geographic safety/proximity analysis near university hubs
- Automated image compression for faster load times

