from configparser import ConfigParser, NoOptionError, NoSectionError
import sys

cfg = ConfigParser()
cfg.read("config.ini")

try:
    APP_ID = cfg.getint("pyrogram", "api_id")
    APP_HASH = cfg.get("pyrogram", "api_hash")
except (NoOptionError, NoSectionError):
    # sys.exit(print('fill in configs before making the session.'))
    print("Find your App configs in https://my.telegram.org")
    APP_ID = int(input("Enter your api_id: "))
    APP_HASH = input("Enter your api_hash: ")
