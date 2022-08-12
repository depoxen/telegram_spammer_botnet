from telethon.sync import TelegramClient
from telethon import functions
from threading import Thread
import asyncio
import toml

with open("config.toml") as file:
    config = toml.load(file)
api_id = config["authorization"]["api_id"]
api_hash = config["authorization"]["api_hash"]
lang = config["locale"]["lang"]


class Channel(Thread):
    def __init__(self, acc, channel, ids, private):
        Thread.__init__(self)
        self.acc = acc
        self.channel = channel
        self.tg_ids = ids
        self.private = private

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        if self.private:
            self.channel = -1000000000000-int(self.channel)
        with TelegramClient("tgaccs/"+self.acc, api_id, api_hash) as client:
            try:
                client(functions.messages.GetMessagesViewsRequest(
                    peer=self.channel,
                    id=self.tg_ids,
                    increment=True
                ))
                if lang == "ru":
                    print(f'{self.acc} посмотрел пост!')
                else:
                    print(f'{self.acc} has seen the post!')
            except:
                if lang == "ru":
                    print(f'{self.acc} не смог посмотреть пост!')
                else:
                    print(f'{self.acc} has not seen the post!')
