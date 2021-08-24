# Generate Pyrogram session via QRlogin

### instructions
- run git clone into a pyrogram project: `git clone https://github.com/pokurt/qr-Pyrogram-session session`
- rename `config.ini.sample` to `config.ini` with your favourite text editor and fill in configs:
    - `mv session/config.ini.sample config.ini && nano config.ini`
- run `pip install -r session/requirements.txt`
- finally run `python -m session -s [session_name]` - session_name: str = 'any name you like to give your Client'
- to get help menu `python -m session -h`

### Features
- modular
- supports bot session and user (qr code) session generation
- can be used as a submodule with git in different pyrogram projects