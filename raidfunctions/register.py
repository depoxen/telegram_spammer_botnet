import re
import datetime
import toml
import os
import asyncio
from telethon.sync import TelegramClient
from telethon import functions
from threading import Thread


with open("config.toml") as file:
    config = toml.load(file)

api_id = config["authorization"]["api_id"]
api_hash = config["authorization"]["api_hash"]
lang = config["locale"]["lang"]


class Register(Thread):
    def __init__(self, acc, func_type, pwd_2fa, old_pwd):
        Thread.__init__(self)
        self.acc = acc
        self.func_type = func_type
        self.pwd_2fa = pwd_2fa
        self.old_pwd = old_pwd

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        if self.func_type == 3:
            self.checkspamblock()
        if self.func_type == 4:
            self.checkvalidation()
        if self.func_type == 5:
            self.auth_2fa()

    def regaccountreg(self):
        try:
            with TelegramClient("tgaccs/" + self.acc, api_id, api_hash) as client:
                client.connect()
            if lang == "ru":
                print('Аккаунт успешно авторизован!')
            else:
                print('Account succesfully authorized!')
        except Exception as err:
            if lang == "ru":
                print(f'Ошибка:\n{err}')
            else:
                print(f'Error:\n{err}')

    def checkcode(self):
        with TelegramClient("tgaccs/" + self.acc, api_id, api_hash) as client:
            result = client(functions.messages.GetHistoryRequest(
                peer=777000,
                offset_id=99999999,
                offset_date=datetime.datetime(2018, 6, 27),
                add_offset=0,
                limit=100,
                max_id=0,
                min_id=0,
                hash=0
            ))
            res = re.findall(r'\d', result.messages[0].message)
            code = ''
            for r in res:
                code += r
            if lang == "ru":
                print(f"Код: {code}")
            else:
                print(f"Code: {code}")

    def checkspamblock(self):
        with TelegramClient("tgaccs/" + self.acc, api_id, api_hash) as client:
            client.send_message(
                "SpamBot",
                message="/start"
            )
            result = client(functions.messages.GetHistoryRequest(
                peer="SpamBot",
                offset_id=99999999,
                offset_date=datetime.datetime(2018, 6, 27),
                add_offset=0,
                limit=100,
                max_id=0,
                min_id=0,
                hash=0
            ))
            result_text = result.messages[0].message
            res_en = result_text.find("Good news")
            res_ru = result_text.find("Ваш аккаунт свободен")
            if res_en == -1 or res_ru == -1:
                res = re.findall(r"\d+\s\w+\s\d{4}", result_text)
                try:
                    if lang == "ru":
                        print(f"{self.acc} в спамблоке до {res[0]}")
                    else:
                        print(f"{self.acc} in spamblock until {res[0]}")
                except:
                    if lang == "ru":
                        print(f"{self.acc} в спамблоке на неопределенный срок")
                    else:
                        print(f"{self.acc} in spamblock until indefinite period")
                os.replace("tgaccs/"+self.acc, "spamblock/"+self.acc)

    def checkvalidation(self):
        if lang == "ru":
            print("Проверка " + self.acc)
        else:
            print("Checking " + self.acc)
        try:
            with TelegramClient("tgaccs/" + self.acc, api_id, api_hash) as client:
                client(functions.messages.GetHistoryRequest(
                    peer=777000,
                    offset_id=99999999,
                    offset_date=datetime.datetime(2018, 6, 27),
                    add_offset=0,
                    limit=100,
                    max_id=0,
                    min_id=0,
                    hash=0
                ))
            if lang == "ru":
                print(f'Аккаунт {self.acc} хороший!')
            else:
                print(f'Account {self.acc} is good!')
        except:
            os.remove("tgaccs/"+self.acc)
            if lang == "ru":
                print(f"Аккаунт в бане: {self.acc}")
            else:
                print(f"This acc in ban: {self.acc}")

    def auth_2fa(self):
        try:
            with TelegramClient("tgaccs/" + self.acc, api_id, api_hash) as client:
                if self.old_pwd == "":
                    client.edit_2fa(new_password=self.pwd_2fa)
                else:
                    client.edit_2fa(current_password=self.old_pwd, new_password=self.pwd_2fa)
            if lang == "ru":
                print(f'2fa пароль ({self.pwd_2fa}) обновлён на аккаунте {self.acc}!')
            else:
                print(f'2fa password ({self.pwd_2fa}) updated on account {self.acc}!')
        except Exception as err:
            if lang == "ru":
                print(f'Ошибка:\n{err}')
            else:
                print(f'Error:\n{err}')
