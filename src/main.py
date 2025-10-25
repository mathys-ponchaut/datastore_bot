import glob

from dependencies.settings import *

from interactions.client.errors import ExtensionNotFound
from interactions import (
    Client,
    Intents,
    listen,
)

bot = Client(intents=Intents.DEFAULT)

@listen()
async def on_ready():
    print(
        f"Bot is ready.\n"
        f"This bot owned by {bot.owner.username}."
    )

    bot.del_unused_app_cmd = True # Delete unused command
    bot.sync_interactions = True

def load(table: Union[str, list]): # Load commands
    """
    Function to load script when bot is launching

    :param table: path to the script to load
    :return:
    """

    def error():
        print(f"Error while loading extensions\n>>> '{str(value)}' wasn't load")

    if isinstance(table, str):
        table = [table]

    if isinstance(table, list):
        for value in table:
            if isinstance(value, str):
                file_found = glob.glob(os.path.join("", "**", f"{value}.py"), recursive=True)

                if file_found:
                    path_to_ext = None
                    for file in file_found:
                        if path_to_ext is None:
                            path_to_ext = f"{str(file)}"
                        else:
                            path_to_ext = f"{str(path_to_ext)}.{str(file)}"

                        path_to_ext = path_to_ext.replace('\\', '.')
                        path_to_ext = path_to_ext.removesuffix(".py")

                        try:
                            bot.load_extension(path_to_ext)
                        except ExtensionNotFound:
                            error()
                else:
                    error()

# Commands
load([
    "upload",
    "search"
])

bot.start(get_setting('token'))