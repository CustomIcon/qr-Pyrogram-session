from .config import APP_ID, APP_HASH
from pyrogram import Client, raw, errors
from time import sleep
from .utils import check_session, clear_screen, _gen_qr, nearest
import sys

ACCEPTED = False


async def raw_handler(client: Client, update: raw.base.Update,  users: list, chats: list):
    if isinstance(update, raw.types.auth.LoginToken):
        if nearest.nearest_dc != await client.storage.dc_id():
            await check_session(client, dc_id=nearest.nearest_dc)
    if isinstance(update, raw.types.UpdateLoginToken):
        try:
            r = await client.send(
                raw.functions.auth.ExportLoginToken(
                    api_id=APP_ID, api_hash=APP_HASH, except_ids=[]
                )
            )
        except errors.exceptions.unauthorized_401.SessionPasswordNeeded as err:
            print(err)
            await client.check_password(input("2FA Password: "))
            r = await client.send(
                raw.functions.auth.ExportLoginToken(
                    api_id=APP_ID, api_hash=APP_HASH, except_ids=[]
                )
            )
        if isinstance(r, raw.types.auth.LoginTokenSuccess):
            me = (await client.get_me()).username
            session_string = await client.export_session_string()
            sys.exit(
                print(
                    f"Generated session for {me}\n\nSessionString:\n{session_string}\n\nquitting..."
                )
            )
        elif isinstance(r, raw.types.auth.LoginTokenMigrateTo):
            await check_session(client, dc_id=r.dc_id)
            r = await client.send(
                    raw.functions.auth.ExportLoginToken(
                        api_id=APP_ID, api_hash=APP_HASH, except_ids=[]
                    )
                )
            if isinstance(r, raw.types.auth.LoginToken):
                clear_screen()
                print('Auth DC Mismatched! please delete the last session and try again')
                _gen_qr(r.token)
                sleep(30)