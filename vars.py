import os


class Config:
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)  # Change None to your OWNER_NAME
    UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "") # Add Your Channel Username without '@'
    DB_URI = os.environ.get("DATABASE_URL", "")
    # List of admin user ids for special functions(
    AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "").split())
