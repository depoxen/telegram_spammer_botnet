import os
from raidfunctions import tgraid
import toml
import time


with open("config.toml") as file:
    config = toml.load(file)
raid_message = config["raid"]["message"]
lang = config["locale"]["lang"]


class Settings:
    def __init__(self, join_chat, username=""):
        self.join_chat = join_chat
        self.username = username

    def get_messages(self, msg_type):
        ms = ""
        if msg_type == 1:
            a = open('args.txt', encoding='utf8')
            ms = a.read().split('\n')
            a.close()
            new_ms = []
            for m in ms:
                if m != "":
                    new_ms.append(self.username+" "+m)
            ms = new_ms
        elif msg_type == 2:
            ms = self.username+" "+raid_message
        return ms

    def start_spam(self):
        tg_accounts = os.listdir('tgaccs')
        if not self.join_chat:
            answ = tgraid.PrepareRaid().questions()
            mentions = False
            if answ[2] == 1:
                if lang == "ru":
                    print("1.Спам предложениями из args.txt\n2.Спам повторяющейся фразой из config.toml\n\n")
                else:
                    print("1.Spam with sentences from args.txt\n2.Repeat phrace from config.toml\n\n")
                msg_type = int(input())
                messages = self.get_messages(msg_type)
                if lang == "ru":
                    mentions_q = int(input("Тегать пользователей?\n1.Да\n2.Нет\n"))
                else:
                    mentions_q = int(input("Tag chat members?\n1.Yes\n2.No\n"))
                if mentions_q == 1:
                    mentions = True
                for account in tg_accounts:
                    if lang == "ru":
                        print(f"Спам запущен с {account} аккаунта!")
                    else:
                        print(f"Spam has been launched from {account} acc!")
                    tgraid.RaidGroup(
                        session_name=account,
                        spam_type=answ[2],
                        files='',
                        messages=messages,
                        chat_id=answ[0],
                        msg_tp=msg_type,
                        speed=answ[1],
                        mentions=mentions
                    ).start()
            if answ[2] == 2:
                if lang == "ru":
                    msg_type = int(input("1.Спам предложениями из args.txt\n2.Спам повторяющейся фразой из config.toml\n\n"))
                    print('Медиа для спам-атаки берутся из папки "raidfiles"')
                else:
                    msg_type = int(input("1.Spam with sentences from args.txt\n2.Repeat phrace from config.toml\n\n"))
                    print('Media for spam is taken from folder "raidfiles"')
                messages = self.get_messages(msg_type)
                files = os.listdir('raidfiles')
                if lang == "ru":
                    mentions_q = int(input("Тегать пользователей?\n1.Да\n2.Нет\n"))
                else:
                    mentions_q = int(input("Tag users?\n1.Yes\n2.No\n"))
                if mentions_q == 1:
                    mentions = True
                for account in tg_accounts:
                    if lang == "ru":
                        print(f"Спам запущен с {account} аккаунта!")
                    else:
                        print(f"Spam has been launched from {account} acc!")
                    tgraid.RaidGroup(
                        session_name=account,
                        spam_type=answ[2],
                        files=files,
                        messages=messages,
                        chat_id=answ[0],
                        msg_tp=msg_type,
                        speed=answ[1],
                        mentions=mentions
                    ).start()
            if answ[2] == 3:
                for account in tg_accounts:
                    if lang == "ru":
                        print(f"Спам запущен с {account} аккаунта!")
                    else:
                        print(f"Spam has been launched from {account} acc!")
                    tgraid.RaidGroup(
                        session_name=account,
                        spam_type=answ[2],
                        files='',
                        messages=[],
                        chat_id=answ[0],
                        msg_tp=0,
                        speed=answ[1],
                        mentions=False
                    ).start()
            if lang == "ru":
                print(
                    'Аккаунты запущены!\n'
                    f'Отправьте команду "{answ[0]}" для запуска спам-атаки!'
                )
            else:
                print(
                    'Accounts has been launched!\n'
                    f'Send command "{answ[0]}" from activating spam!'
                )
        else:
            if lang == "ru":
                link_to_chat = input('Введи ссылку на чат: ')
                captcha_q = int(input('Решать капчу?\n1.Да\n2.Нет\n'))
            else:
                link_to_chat = input('Enter chat link: ')
                captcha_q = int(input('Solve captcha?\n1.Yes\n2.No\n'))
            captcha = 0
            if captcha_q == 1:
                if lang == "ru":
                    captcha = int(input('Вид капчи:\n1.Кнопка\n2.Математический пример\n'))
                else:
                    captcha = int(input('Captcha type:\n1.Button\n2.Math example\n'))

            for tg_acc in tg_accounts:
                tgraid.ConfJoin(
                    accs=tg_acc,
                    chat_link=link_to_chat,
                    captcha=captcha
                ).start()
                if captcha_q == 1:
                    time.sleep(5)
