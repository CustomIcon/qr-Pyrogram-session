from base64 import urlsafe_b64encode as base64url
from configparser import ConfigParser, NoOptionError, NoSectionError
from time import sleep
import logging
import sys
from pyrogram import Client, errors
from pyrogram.raw import base, functions, types
from pyrogram.session import Session, Auth
from qrcode import QRCode
import os
from subprocess import call


logging.basicConfig(level=logging.INFO)
cfg = ConfigParser()
cfg.read("config.ini")
qr = QRCode()

try:
    APP_ID = cfg.getint("pyrogram", "api_id")
    APP_HASH = cfg.get("pyrogram", "api_hash")
except (NoOptionError, NoSectionError):
    sys.exit(print('fill in configs before making the session.'))


app = Client(sys.argv[1], app_version="SCP-5170")
app.connect()
app.initialize()
nearest = app.send(functions.help.GetNearestDc())


ACCEPTED = False

def clear_screen():
    call(['cls' if os.name == 'nt' else 'clear'], shell=True)


@app.on_raw_update()
async def raw_handler(client: Client, update: base.Update):
    global ACCEPTED
    if isinstance(update, types.auth.LoginToken):
        if nearest.nearest_dc != await client.storage.dc_id():
            await check_session(client, dc_id=nearest.nearest_dc)
    if isinstance(update, types.UpdateLoginToken):
        ACCEPTED = True
        try:
            r = await app.send(
                functions.auth.ExportLoginToken(
                    api_id=APP_ID, api_hash=APP_HASH, except_ids=[]
                )
            )
        except errors.exceptions.unauthorized_401.SessionPasswordNeeded as err:
            print(err)
            await app.check_password(input("2FA Password: "))
            r = await app.send(
                functions.auth.ExportLoginToken(
                    api_id=APP_ID, api_hash=APP_HASH, except_ids=[]
                )
            )
        if isinstance(r, types.auth.LoginTokenSuccess):
            me = (await app.get_me()).username
            sys.exit(print(f"Generated session for {me}\n\ quitting..."))
        elif isinstance(r, types.auth.LoginTokenMigrateTo):
            await check_session(app, dc_id=r.dc_id)
            r = await app.send(
                    functions.auth.ExportLoginToken(
                        api_id=APP_ID, api_hash=APP_HASH, except_ids=[]
                    )
                )
            if isinstance(r, types.auth.LoginToken):
                clear_screen()
                print('Auth DC Mismatched! please delete the last session and try again')
                _gen_qr(r.token)
                sleep(30)


async def check_session(
    client: Client,
    dc_id:int
):
    await client.session.stop()
    await client.storage.dc_id(dc_id)
    await client.storage.auth_key(
        await Auth(
            client, await client.storage.dc_id(),
            await client.storage.test_mode()
        ).create()
    )
    client.session = Session(
        client, await client.storage.dc_id(),
        await client.storage.auth_key(), await client.storage.test_mode()
    )
    return await client.session.start()


def create_qrcodes():
    while True:
        clear_screen()
        print(
            'Scan the QR code below:'
        )
        print(
            'Settings > Privacy and Security > Active Sessions > Scan QR Code'
        )
        if ACCEPTED:
            break
        r = app.send(
            functions.auth.ExportLoginToken(
                api_id=APP_ID, api_hash=APP_HASH, except_ids=[]
            )
        )
        if isinstance(r, types.auth.LoginToken):
            _gen_qr(r.token)
            sleep(30)


def _gen_qr(token:bytes):
    token = base64url(token).decode("utf8")
    login_url = "tg://login?token=" + token
    qr.clear()
    qr.add_data(login_url)
    qr.print_ascii()