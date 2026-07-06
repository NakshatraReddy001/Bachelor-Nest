import re

AMENITY_KEYS = ("WiFi", "AC", "Laundry", "Parking", "Food / Mess", "Gym")

def is_valid_gmail(email: str) -> bool:
    """Strict evaluation enforcing standard @gmail.com formatting."""
    pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@gmail\.com$")
    return bool(pattern.match(email.strip()))