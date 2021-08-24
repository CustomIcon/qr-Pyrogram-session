from configparser import ConfigParser, NoOptionError, NoSectionError
import sys

cfg = ConfigParser()
cfg.read("config.ini")

try:
    APP_ID = cfg.getint("pyrogram", "api_id")
    APP_HASH = cfg.get("pyrogram", "api_hash")
except (NoOptionError, NoSectionError):
    sys.exit(print('fill in configs before making the session.'))