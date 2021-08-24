from .config import APP_HASH, APP_ID
from pyrogram import Client
from .Colored import ColoredArgParser
from .args import args as Args
parser = ColoredArgParser()
for arg in Args:
    parser.add_argument(
        arg['short_name'],
        arg['long_name'],
        help=arg['help'],
        type=arg['type']
    )
args = parser.parse_args()

app = Client(args.session_name or "pyrogram", api_id=APP_ID, api_hash=APP_HASH)