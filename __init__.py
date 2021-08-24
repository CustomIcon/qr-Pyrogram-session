import logging
import sys
from pyrogram import Client, errors, handlers
from .updater import raw_handler
from .client import app
from .config import APP_ID, APP_HASH
from .client import args



logging.basicConfig(level=logging.INFO)


if args.token:
    app = Client(
        args.session_name or str(__package__),
        api_id=APP_ID,
        api_hash=APP_HASH,
        bot_token=args.token
    )
    try:
        app.start()
    except (
        errors.AccessTokenInvalid,
        errors.AccessTokenExpired,
        errors.AuthKeyUnregistered
    ) as err:
        sys.exit(print(err))
    me = app.get_me().first_name
    app.stop()
    sys.exit(print(f"Generated session for {me}\n\n quitting..."))

app.add_handler(
    handlers.RawUpdateHandler(
        raw_handler
    )
)

