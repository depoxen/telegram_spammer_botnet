import asyncio
import time
import random
import toml
from threading import Thread
from telethon.sync import TelegramClient, events
from telethon import functions, types
from telethon.tl.functions.messages import GetAllStickersRequest
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import InputStickerSetID


with open("config.toml") as file:
    config = toml.load(file)

api_id = config["authorization"]["api_id"]
api_hash = config["authorization"]["api_hash"]
raid_message = config["raid"]["message"]
lang = config["locale"]["lang"]


class PrepareRaid:
    def __init__(self):
        pass

    @staticmethod
    def questions():
        answlist = []
        if lang == "ru":
            msg_link = input('Скопируй и вставь ссылку на сообщение в чате: ').split("/")
        else:
            msg_link = input('Copy and paste message link from chat: ').split("/")
        chat = msg_link[3]
        if msg_link[3] == "c":
            chat = (int(msg_link[4]) + 1000000000000) * -1
        answlist.append(chat)
        if lang == "ru":
            answlist.append(int(input('Скорость атаки:\n1.Быстро\n2.Медленно\n')))
            answlist.append(int(input('1.Спамить текстом\n2.Спамить медиафайлами\n3.Спам стикерами\n')))
        else:
            answlist.append(int(input('Spam speed:\n1.Fast\n2.Slow\n')))
            answlist.append(int(input('1.Spam via text\n2.Spam via media\n3.Sticker spam\n')))
        return answlist


class LsRaid(Thread):
    def __init__(self, user_id, session_name, msg_tp, messages, spam_type, files=None):
        Thread.__init__(self)
        if files is None:
            files = []
        self.user_id = user_id
        self.session_name = session_name
        self.msg_tp = msg_tp
        self.messages = messages
        self.spam_type = spam_type
        self.files = files

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = TelegramClient("tgaccs/" + self.session_name, api_id, api_hash)
        client.start()
        count = 1
        while True:
            try:
                if self.spam_type == 1:
                    if self.msg_tp == 1:
                        msg = random.choice(self.messages[:4096])
                        if msg != '':
                            client(
                                functions.messages.SendMessageRequest(
                                    peer=self.user_id,
                                    message=msg
                                )
                            )
                    else:
                        client(
                            functions.messages.SendMessageRequest(
                                peer=self.user_id,
                                message=self.messages[:4096]
                            )
                        )
                if self.spam_type == 2:
                    if self.msg_tp == 1:
                        msg = random.choice(self.messages[:4096])
                        if msg != '':
                            client.send_file(
                                self.user_id,
                                f"raidfiles/{random.choice(self.files)}",
                                caption=msg
                            )
                    else:
                        msg = self.messages[:4096]
                        client.send_file(
                            self.user_id,
                            f"raidfiles/{random.choice(self.files)}",
                            caption=msg
                        )
                if self.spam_type == 3:
                    sticker_sets = client(GetAllStickersRequest(0))
                    sticker_set = random.choice(sticker_sets.sets)
                    stickers = client(GetStickerSetRequest(
                        stickerset=InputStickerSetID(
                            id=sticker_set.id, access_hash=sticker_set.access_hash
                        )
                    ))
                    client.send_file(self.user_id, random.choice(stickers.documents))
                if lang == "ru":
                    print(f"[PM SPAM] Отправлено {count} раз с аккаунта {self.session_name}!")
                else:
                    print(f"[PM SPAM] Sended {count} times from acc {self.session_name}!")
            except Exception as er:
                if lang == "ru":
                    print(f"[PM RAID] Ошибка в {self.session_name}:\n{er}")
                else:
                    print(f"[PM RAID] Error in {self.session_name}:\n{er}")
                break
            count += 1
            time.sleep(0.1)
        client.disconnect()


class RaidGroup(Thread):
    def __init__(self, session_name, spam_type, files, messages, chat_id, msg_tp, speed, mentions):
        Thread.__init__(self)
        self.session_name = session_name
        self.spam_type = spam_type
        self.files = files
        self.messages = messages
        self.chat_id = chat_id
        self.msg_tp = msg_tp
        self.speed = speed
        self.mentions = mentions

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = TelegramClient("tgaccs/"+self.session_name, api_id, api_hash)
        client.start()

        users = None
        if self.mentions:
            users = client.get_participants(self.chat_id)
        count = 1
        while True:
            try:
                if self.spam_type == 1:
                    if self.msg_tp == 1:
                        msg = random.choice(self.messages)
                        if self.mentions:
                            user = random.choice(users)
                            msg = f"<a href='tg://user?id={user.id}'>.</a> {msg}"
                        if msg != '':
                            client.send_message(
                                self.chat_id,
                                message=msg[:4096],
                                parse_mode="html"
                            )
                    else:
                        msg = self.messages[:4056]
                        if self.mentions:
                            user = random.choice(users)
                            msg = f"<a href='tg://user?id={user.id}'>.</a> {self.messages[:4056]}"
                        client.send_message(
                            self.chat_id,
                            message=msg,
                            parse_mode="html"
                        )
                if self.spam_type == 2:
                    if self.msg_tp == 1:
                        msg = random.choice(self.messages)
                        if self.mentions:
                            user = random.choice(users)
                            msg = f"<a href='tg://user?id={user.id}'>.</a> {msg}"
                        if msg != '':
                            client.send_file(
                                self.chat_id,
                                f"raidfiles/{random.choice(self.files)}",
                                caption=msg[:4096],
                                parse_mode="html"
                            )
                    else:
                        msg = self.messages[:4056]
                        if self.mentions:
                            user = random.choice(users)
                            msg = f"<a href='tg://user?id={user.id}'>.</a> {self.messages[:4056]}"
                        client.send_file(
                            self.chat_id,
                            f"raidfiles/{random.choice(self.files)}",
                            caption=msg,
                            parse_mode="html"
                        )
                if self.spam_type == 3:
                    sticker_sets = client(GetAllStickersRequest(0))
                    sticker_set = random.choice(sticker_sets.sets)
                    stickers = client(GetStickerSetRequest(
                        stickerset=InputStickerSetID(
                            id=sticker_set.id, access_hash=sticker_set.access_hash
                        )
                    ))
                    client.send_file(self.chat_id, random.choice(stickers.documents))
                if self.speed == 1:
                    time.sleep(0.1)
                if self.speed == 2:
                    time.sleep(random.randint(7, 10))
                if lang == "ru":
                    print(f"[GROUP RAID] Отправлено {count} раз с аккаунта {self.session_name}!")
                else:
                    print(f"[GROUP RAID] Sended {count} times from acc {self.session_name}!")
            except Exception as er:
                if lang == "ru":
                    print(f"[GROUP RAID] Ошибка в {self.session_name}:\n{er}")
                else:
                    print(f"[GROUP RAID] Sended {count} times from acc {self.session_name}!")
                break
            count += 1
        client.disconnect()


class ConfJoin(Thread):
    def __init__(self, accs, chat_link, captcha):
        Thread.__init__(self)
        self.accs = accs
        self.chat_link = chat_link
        self.captcha = captcha

    def run(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            with TelegramClient("tgaccs/"+self.accs, api_id, api_hash) as client:
                client.connect()
                if self.chat_link[:1] == '@':
                    chat = client.get_entity(self.chat_link[1:])
                    client(functions.channels.JoinChannelRequest(chat.id))
                try:
                    if self.chat_link[:13] == 'https://t.me/':
                        chat = client.get_entity(self.chat_link[13:])
                        client(functions.channels.JoinChannelRequest(chat.id))
                except:
                    pass
                if self.chat_link[13:14] == '+':
                    client(functions.messages.ImportChatInviteRequest(hash=self.chat_link[14:]))
                if self.chat_link[13:21] == 'joinchat':
                    client(functions.messages.ImportChatInviteRequest(hash=self.chat_link[22:]))
                if self.captcha == 1:
                    try:
                        @client.on(events.NewMessage)
                        async def my_event_handler(event):
                            if event.mentioned:
                                kb = event.reply_markup
                                for x in range(len(kb.rows)):
                                    try:
                                        a = kb.rows[x].buttons[0].data
                                        print(a)
                                        await event.click(x)
                                        await client.disconnect()
                                    except:
                                        pass
                            else:
                                kb = event.reply_markup
                                for x in range(len(kb.rows)):
                                    try:
                                        a = kb.rows[x].buttons[0].data
                                        print(a)
                                        await event.click(x)
                                        await client.disconnect()
                                    except:
                                        pass
                        client.start()
                        client.run_until_disconnected()
                    except:
                        pass
                if self.captcha == 2:
                    try:
                        @client.on(events.NewMessage)
                        async def my_event_handler(event):
                            if event.mentioned:
                                text = event.text
                                end = text.find(")")
                                b = text[1:end].replace(' ', '')
                                nums = b.split("+")
                                answ = str(int(nums[0])+int(nums[1]))
                                await client.send_message(
                                    event.chat_id,
                                    message=answ,
                                )
                                await client.disconnect()
                        client.start()
                        client.run_until_disconnected()
                    except:
                        pass
                client.disconnect()
            if lang == "ru":
                print(f"{self.accs} успешно зашел в чат!")
            else:
                print(f"{self.accs} successfully joined the chat!")
            del client
        except Exception as err:
            if lang == "ru":
                print(f"{self.accs} не смог зайти в чат. Причина:\n{err}")
            else:
                print(f"{self.accs} can't join the chat. Reason:\n{err}")


class RaidComments(Thread):
    def __init__(self, channel, session_name, msg_tp, messages, spam_type, post_id, speed, files=None):
        Thread.__init__(self)
        self.channel = channel
        self.session_name = session_name
        self.msg_tp = msg_tp
        self.messages = messages
        self.spam_type = spam_type
        self.post_id = int(post_id)
        self.speed = speed
        self.files = files

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = TelegramClient("tgaccs/" + self.session_name, api_id, api_hash)
        client.start()
        channel_id = self.channel
        count = 1
        try:
            channel_id = int(channel_id)
            channel_id = (1000000000000+channel_id)*-1
            client.get_entity(channel_id)
        except:
            pass
        while True:
            try:
                if self.spam_type == 1:
                    if self.msg_tp == 1:
                        msg = random.choice(self.messages)
                        if msg != '':
                            client.send_message(
                                channel_id,
                                message=msg[:4096],
                                comment_to=self.post_id
                            )
                    else:
                        msg = self.messages[:4096]
                        client.send_message(
                            channel_id,
                            message=msg,
                            comment_to=self.post_id
                        )
                if self.spam_type == 2:
                    if self.msg_tp == 1:
                        msg = random.choice(self.messages)
                        if msg != '':
                            client.send_file(
                                channel_id,
                                f"raidfiles/{random.choice(self.files)}",
                                caption=msg[:4096],
                                comment_to=self.post_id
                            )
                    else:
                        msg = self.messages[:4096]
                        client.send_file(
                            channel_id,
                            f"raidfiles/{random.choice(self.files)}",
                            caption=msg,
                            comment_to=self.post_id
                        )
                if lang == "ru":
                    print(f"[COMMENTS RAID] Отправлено {count} раз с аккаунта {self.session_name}!")
                else:
                    print(f"[COMMENTS RAID] Sended {count} times from account {self.session_name}!")
            except Exception as er:
                if lang == "ru":
                    print(f"[COMMENTS RAID] Ошибка в {self.session_name}:\n{er}")
                else:
                    print(f"[COMMENTS RAID] Error in {self.session_name}:\n{er}")
                break
            count += 1
            if self.speed == 1:
                time.sleep(0.1)
            if self.speed == 2:
                time.sleep(random.randint(7, 10))
        client.disconnect()


class PhoneLsRaid(Thread):
    def __init__(self, phone_tg, session_name, msg_tp, messages, spam_type, files=None):
        Thread.__init__(self)
        self.phone_tg = phone_tg
        self.session_name = session_name
        self.msg_tp = msg_tp
        self.messages = messages
        self.spam_type = spam_type
        self.files = files

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = TelegramClient("tgaccs/" + self.session_name, api_id, api_hash)
        client.start()
        count = 1
        result = client(functions.contacts.ImportContactsRequest(
            contacts=[types.InputPhoneContact(
                client_id=random.randint(1, 9999),
                first_name="name",
                last_name="surname",
                phone=self.phone_tg
            )]
        ))
        user_id = result.users[0].id
        while True:
            try:
                if self.spam_type == 1:
                    if self.msg_tp == 1:
                        msg = random.choice(self.messages)
                        if msg != '':
                            client(
                                functions.messages.SendMessageRequest(
                                    peer=user_id,
                                    message=msg[:4096]
                                )
                            )
                    else:
                        msg = self.messages[:4096]
                        client(
                            functions.messages.SendMessageRequest(
                                peer=user_id,
                                message=msg
                            )
                        )
                if self.spam_type == 2:
                    if self.msg_tp == 1:
                        msg = random.choice(self.messages)
                        if msg != '':
                            client.send_file(
                                user_id,
                                f"raidfiles/{random.choice(self.files)}",
                                caption=msg[:4096]
                            )
                    else:
                        msg = self.messages[:4096]
                        client.send_file(
                            user_id,
                            f"raidfiles/{random.choice(self.files)}",
                            caption=msg
                        )
                if self.spam_type == 3:
                    sticker_sets = client(GetAllStickersRequest(0))
                    sticker_set = random.choice(sticker_sets.sets)
                    stickers = client(GetStickerSetRequest(
                        stickerset=InputStickerSetID(
                            id=sticker_set.id, access_hash=sticker_set.access_hash
                        )
                    ))
                    client.send_file(user_id, random.choice(stickers.documents))
                if lang == "ru":
                    print(f"[PM PHONE RAID] Отправлено {count} раз с аккаунта {self.session_name}!")
                else:
                    print(f"[PM PHONE RAID] Sended {count} times from acc {self.session_name}!")
            except Exception as er:
                if lang == "ru":
                    print(f"[PM PHONE RAID] Ошибка в {self.session_name}:\n{er}")
                else:
                    print(f"[PM PHONE RAID] Error in {self.session_name}:\n{er}")
                break
            count += 1
            time.sleep(0.1)
        client.disconnect()


class ForwardSpam(Thread):
    def __init__(self, session_name, chat, post_id, spam_chat):
        Thread.__init__(self)
        self.session_name = session_name
        self.chat = chat
        self.post_id = int(post_id)
        self.spam_chat = spam_chat

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = TelegramClient("tgaccs/" + self.session_name, api_id, api_hash)
        client.start()
        count = 1
        while True:
            try:
                client(
                    functions.messages.ForwardMessagesRequest(
                        from_peer=self.chat,
                        id=[self.post_id],
                        to_peer=self.spam_chat
                    )
                )
                if lang == "ru":
                    print(f"[FORWARD RAID] Отправлено {count} раз с аккаунта {self.session_name}!")
                else:
                    print(f"[FORWARD RAID] Sended {count} times from acc {self.session_name}!")
            except Exception as e:
                if lang == "ru":
                    print(f"[FORWARD RAID] Ошибка в {self.session_name}:\n{e}")
                else:
                    print(f"[FORWARD RAID] Error in {self.session_name}:\n{e}")
                break
            count += 1
            time.sleep(0.1)
        client.disconnect()
