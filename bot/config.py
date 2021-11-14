from sys import argv as arguments
from os import path, mkdir


DEBUG = "debug" in arguments
PRODUCTION_GROUP_ID = 185313238
DEBUG_GROUP_ID = 0
PRODUCTION_TOKEN = ""
DEBUG_TOKEN = ""

GROUP_ID = None
TOKEN = None

if DEBUG:
    print("Starting witless in DEBUG mode...")
    TOKEN = DEBUG_TOKEN
    GROUP_ID = DEBUG_GROUP_ID

else:
    print("Starting witless in PRODUCTION mode...")
    TOKEN = PRODUCTION_TOKEN
    GROUP_ID = PRODUCTION_GROUP_ID


if not path.exists("messages"):
    mkdir("messages")
