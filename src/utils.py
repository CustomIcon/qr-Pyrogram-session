from pyrogram.session import Session, Auth
from pyrogram import Client, raw
import os
from qrcode import QRCode
from base64 import urlsafe_b64encode as base64url
from time import sleep
from subprocess import call
from .config import APP_ID, APP_HASH
from .client import app

qr = QRCode()


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


def clear_screen():
    call(['cls' if os.name == 'nt' else 'clear'], shell=True)


def create_qrcodes():
    while True:
        clear_screen()
        print(
            'Scan the QR code below:'
        )
        print(
            'Settings > Privacy and Security > Active Sessions > Scan QR Code'
        )
        r = app.send(
            raw.functions.auth.ExportLoginToken(
                api_id=APP_ID, api_hash=APP_HASH, except_ids=[]
            )
        )
        if isinstance(r, raw.types.auth.LoginToken):
            _gen_qr(r.token)
            sleep(30)


def _gen_qr(token:bytes):
    token = base64url(token).decode("utf8")
    login_url = "tg://login?token=" + token
    qr.clear()
    qr.add_data(login_url)
    qr.print_ascii()

app.connect()
app.initialize()
nearest = app.send(raw.functions.help.GetNearestDc())