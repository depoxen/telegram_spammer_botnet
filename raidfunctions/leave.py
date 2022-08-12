from threading import Thread
import asyncio
import toml
from telethon.sync import TelegramClient
from telethon import functions, types


with open("config.toml") as file:
    config = toml.load(file)
api_id = config["authorization"]["api_id"]
api_hash = config["authorization"]["api_hash"]
lang = config["locale"]["lang"]


class Leave(Thread):
    def __init__(self, acc, channel_id):
        Thread.__init__(self)
        self.acc = acc
        self.channel_id = channel_id

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        with TelegramClient("tgaccs/"+self.acc, api_id, api_hash) as client:
            try:
                client.connect()
                client.get_entity(self.channel_id)
                client(functions.channels.LeaveChannelRequest(self.channel_id))
                client.disconnect()
            except:
                pass
        del client
        if lang == "ru":
            print(f"{self.acc} вышел")
        else:
            print(f"{self.acc} left")


class LeaveChat:
    def __init__(self, acc):
        self.acc = acc

    def start(self):
        with TelegramClient("tgaccs/"+self.acc, api_id, api_hash) as client:
            try:
                client.connect()
                for dialog in client.iter_dialogs():
                    if not isinstance(dialog.entity, types.Channel):
                        client(functions.messages.DeleteHistoryRequest(
                            peer=dialog.entity,
                            max_id=0,
                            just_clear=True,
                            revoke=True
                        ))
                    else:
                        client(
                            functions.channels.LeaveChannelRequest(dialog.id)
                        )
            except:
                pass
        if lang == "ru":
            print(f"Диалоги были удалены с {self.acc}!")
        else:
            print(f"Dialogs has been deleted from {self.acc}!")
