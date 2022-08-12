import os
from raidfunctions import register, tgraid
from raidfunctions import additional, start_spam
from raidfunctions import report, addsticker
from raidfunctions import leave, see
from raidfunctions import polls, joinleave
import toml
try:
    import ctypes
    libgcc_s = ctypes.CDLL('libgcc_s.so.1')
except:
    pass
with open("config.toml") as file:
    config = toml.load(file)
lang = config["locale"]["lang"]

print(
    "=======================\n\n"
    "TGRAID\n\n"
    "=======================\n"
)
if lang == "ru":
    menu = \
        'После выполнения операции перезапускайте программу!\n'\
        'Выбирайте операцию:\n\n'\
        '0.Зарегать акк или авторизовать\n'\
        '1.Рейд (спам-атака аккаунтами)\n'\
        '2.Зайти в чат / подписаться на канал\n'\
        '3.Отправить жб на сообщения или посты\n'\
        '4.Добавление или удаление стикеров\n'\
        '5.Другие функции\n'\
        '6.Накрутка просмотров на пост\n'\
        '7.Проголосовать в опросе\n'
    raidmenu = \
        '1.Заспамить чат\n'\
        '2.Спам в лс тг\n'\
        '3.Спам в комменты под пост\n'\
        '4.Спам в лс с помощью импорта контакта по номеру\n'\
        '5.Спам пересыланием сообщения / поста\n'\
        '6.Спам входом / выходом из чата\n'\
        '7.Спам теганьем одного человека\n'\
        '8.Выйти из чата / канала\n'
else:
    menu = \
        'After operation restart program!\n'\
        'Choose operation:\n\n'\
        '0.Register or authorize acc\n'\
        '1.Raid (acc spam attack)\n'\
        '2.Join a chat/channel\n'\
        '3.Send reports to message or post\n'\
        '4.Add or remove stickers\n'\
        '5.Other functions\n'\
        '6.Increase views\n'\
        '7.Vote in a poll\n'
    raidmenu = \
        '1.Spam a chat\n'\
        '2.Spam in private chat to user\n'\
        "3.Spam in channel's comments\n"\
        '4.Spam in private chat to user via contact input\n'\
        '5.Spam with forwarding message or post\n'\
        '6.Join/Leave spam\n'\
        '7.Spam with mention to one user\n'\
        '8.Leave chat/channel\n'


for filename in os.listdir("tgaccs"):
    if filename.endswith(".session-journal"):
        os.remove(
            os.path.join("tgaccs", filename)
        )
acc_count = len(os.listdir("tgaccs"))
spamblock = len(os.listdir("spamblock"))
if lang == "ru":
    print(f"Количество активных аккаунтов: {acc_count}")
    print(f"Аккаунты в спамблоке: {spamblock}")
else:
    print(f"Count of active accs: {acc_count}")
    print(f"Accs in spamblock: {spamblock}")

while True:
    try:
        accs = os.listdir('tgaccs')
        a = int(input(menu))
        if a == 0:
            while True:
                if lang == "ru":
                    print(
                        '1)Авторизовать аккаунт или зарегистрировать\n'
                        '2)Получить код активации из сессии\n'
                        '3)Проверить валидность аккаунтов\n'
                        '4)Проверить наличие акков в спамблоке\n'
                        '5)Установить или убрать пароль на аккаунтах\n'
                    )
                else:
                    print(
                        '1)Authorize acc or register\n'
                        '2)Get activation code for authorization\n'
                        '3)Check accs validation\n'
                        '4)Check accs spamblock\n'
                        '5)Set 2fa auth on accounts\n'
                    )
                c = int(input())
                accounts = os.listdir('tgaccs')
                if c == 1:
                    if lang == "ru":
                        name = input("Введи номер от аккаунта:\n")
                    else:
                        name = input("Enter phone number from acc:\n")
                    register.Register(name, 1, None, None).regaccountreg()
                elif c == 2:
                    if lang == "ru":
                        print("Введи номер от аккаунта\n")
                    else:
                        print("Enter phone number from acc\n")
                    name = input()
                    register.Register(name, 2, None, None).checkcode()
                elif c == 3:
                    for account in accounts:
                        register.Register(account, 4, None, None).start()
                elif c == 4:
                    for account in accounts:
                        register.Register(account, 3, None, None).start()
                elif c == 5:
                    if lang == "ru":
                        old_pwd = input("Введи старый пароль (если есть):\n")
                    else:
                        old_pwd = input("Enter old password (if exists):\n")
                    if lang == "ru":
                        pwd = input("Введи новый пароль:\n")
                    else:
                        pwd = input("Enter new password:\n")
                    for account in accounts:
                        register.Register(account, 5, pwd, old_pwd).start()
        elif a == 1:
            b = int(input(raidmenu))
            if b == 1:
                spam = start_spam.Settings(False)
                spam.start_spam()
            elif b == 2:
                if lang == "ru":
                    idtg = input("Введи юзернем куда спам делать:\n")
                    spam_type = int(input("1.Спамить текстом\n2.Спамить медиафайлами\n3.Спам стикерами\n"))
                    msg_tp = int(input("1.Спам предложениями из args.txt\n2.Спам повторяющейся фразой из config.toml\n\n"))
                else:
                    idtg = input("Enter person's username\n")
                    spam_type = int(input("1.Spam via text\n2.Spam via media\n3.Sticker spam\n"))
                    msg_tp = int(input("1.Spam with sentences from args.txt\n2.Repeat phrace from config.toml\n\n"))
                files = []
                if spam_type in [1, 2]:
                    msg = start_spam.Settings(False).get_messages(msg_tp)
                else:
                    msg = ''
                if spam_type == 2:
                    files = os.listdir('raidfiles')
                for acc in accs:
                    try:
                        if lang == "ru":
                            print(f"Спам запусщен с {acc} аккаунта!")
                        else:
                            print(f"Spam has been launched from {acc} acc!")
                        tgraid.LsRaid(
                            user_id=idtg,
                            session_name=acc,
                            msg_tp=msg_tp,
                            messages=msg,
                            files=files,
                            spam_type=spam_type
                        ).start()
                    except:
                        pass
            elif b == 3:
                if lang == "ru":
                    idtg = input("Введите ссылку на пост:\n").split("/")
                    spam_type = int(input("1.Спамить текстом\n2.Спамить медиафайлами\n3.Спам стикерами\n"))
                    msg_tp = int(input("1.Спам предложениями из args.txt\n2.Спам повторяющейся фразой из config.toml\n\n"))
                else:
                    idtg = input("Enter post link:\n").split("/")
                    spam_type = int(input("1.Spam via text\n2.Spam via media\n3.Sticker spam\n"))
                    msg_tp = int(input("1.Spam with sentences from args.txt\n2.Repeat phrace from config.toml\n\n"))
                channel = idtg[3]
                post_id = idtg[4]
                files = []
                if channel == 'c':
                    channel = idtg[4]
                    post_id = idtg[5]
                msg = start_spam.Settings(False).get_messages(msg_tp)
                if spam_type == 2:
                    files = os.listdir('raidfiles')
                if lang == "ru":
                    print("Скорость атаки:\n1.Быстро\n2.Медленно")
                else:
                    print("Spam speed:\n1.Fast\n2.Slow")
                speed = int(input())
                for acc in accs:
                    try:
                        if lang == "ru":
                            print(f"Спам запусщен с {acc} аккаунта!")
                        else:
                            print(f"Spam has been launched from {acc} acc!")
                        tgraid.RaidComments(
                            channel=channel,
                            session_name=acc,
                            msg_tp=msg_tp,
                            messages=msg,
                            spam_type=spam_type,
                            post_id=post_id,
                            files=files,
                            speed=speed
                        ).start()
                    except:
                        pass
            elif b == 4:
                if lang == "ru":
                    phonetg = input("Введи номер телефона жертвы\n")
                else:
                    phonetg = input("Enter victim's phone number\n")
                phone_tg = ""
                for s in phonetg:
                    if s not in [" ", "(", ")"]:
                        phone_tg += s
                print(phone_tg)
                files = []
                if lang == "ru":
                    spam_type = int(input("1.Спамить текстом\n2.Спамить медиафайлами\n3.Спам стикерами\n"))
                else:
                    spam_type = int(input("1.Spam via text\n2.Spam via media\n3.Sticker spam\n"))
                if spam_type == 1:
                    if lang == "ru":
                        msg_tp = int(input("1.Спам предложениями из args.txt\n2.Спам повторяющейся фразой из config.toml\n\n"))
                    else:
                        msg_tp = int(input("1.Spam with phraces from args.txt\n2.Repeat phrace from config.toml\n\n"))
                    msg = start_spam.Settings(False).get_messages(msg_tp)
                else:
                    if lang == "ru":
                        msg_tp = int(input("1.Спам предложениями из args.txt\n2.Спам повторяющейся фразой из config.toml\n\n"))
                    else:
                        msg_tp = int(input("1.Spam with phraces from args.txt\n2.Repeat phrace from config.toml\n\n"))
                    msg = start_spam.Settings(False).get_messages(msg_tp)
                    files = os.listdir('raidfiles')
                for acc in accs:
                    try:
                        if lang == "ru":
                            print(f"Спам запусщен с {acc} аккаунта!")
                        else:
                            print(f"Spam has been launched from {acc} acc!")
                        tgraid.PhoneLsRaid(
                            phone_tg=phone_tg,
                            session_name=acc,
                            msg_tp=msg_tp,
                            messages=msg,
                            files=files,
                            spam_type=spam_type
                        ).start()
                    except:
                        pass
            elif b == 5:
                if lang == "ru":
                    fwd_link = input('Скопируй и вставь ссылку на сообщение, которое надо переслать в чате: ').split("/")
                    msg_link = input('Скопируй и вставь ссылку на сообщение в чате: ').split("/")
                else:
                    fwd_link = input('Copy and paste forwadding message link from chat: ').split("/")
                    msg_link = input('Copy and paste message link from chat: ').split("/")
                chat = fwd_link[3]
                post_id = fwd_link[4]
                if fwd_link[3] == "c":
                    chat = (int(fwd_link[4]) + 1000000000000) * -1
                    post_id = fwd_link[5]
                spam_chat = msg_link[3]
                if msg_link[3] == "c":
                    spam_chat = (int(msg_link[4]) + 1000000000000) * -1
                for acc in accs:
                    try:
                        tgraid.ForwardSpam(
                            session_name=acc,
                            chat=chat,
                            post_id=post_id,
                            spam_chat=spam_chat
                        ).start()
                    except:
                        pass
            elif b == 6:
                if lang == "ru":
                    link_to_chat = input('Введи ссылку на чат: ')
                    print("Скопируй ссылку на пост или на сообщение: ")
                else:
                    link_to_chat = input('Enter chat link: ')
                    print("Copy message or post link:")
                msg_link = input()
                joinleave.JoinLeave(accs, msg_link, link_to_chat).start()
            elif b == 7:
                if lang == "ru":
                    print("1.Тегать юзернеймом\n2.Тегнуть через телеграм айди")
                else:
                    print("1.Mention via username\n2.Mention via telegram id")
                ch = int(input())
                if ch == 1:
                    if lang == "ru":
                        print("Ввести юзернейм с @")
                    else:
                        print("Enter username with @")
                    username = input()
                elif ch == 2:
                    if lang == "ru":
                        print("Ввести айди телеграм")
                    else:
                        print("Enter telegram id")
                    username = f"<a href='tg://user?id={input()}'>.</a>"
                else:
                    username = ""
                spam = start_spam.Settings(False, username)
                spam.start_spam()
            elif b == 8:
                if lang == "ru":
                    print("Скопируй ссылку на пост или на сообщение: ")
                else:
                    print("Copy message or post link:")
                post = input().split("/")
                channel = post[3]
                if post[3] == "c":
                    channel = (int(post[4])+1000000000000)*-1
                for acc in accs:
                    try:
                        leave.Leave(acc, channel).start()
                    except:
                        pass
        elif a == 2:
            spam = start_spam.Settings(True)
            spam.start_spam()
        elif a == 3:
            post_ids = []
            if lang == "ru":
                msg_link = input('Введи ссылку на пост или на сообщение: ').split("/")
            else:
                msg_link = input('Copy and paste message link from chat: ').split("/")
            channel = msg_link[3]
            post_id = msg_link[4]
            if msg_link[3] == "c":
                channel = (int(msg_link[4]) + 1000000000000) * -1
                post_id = msg_link[5]
            post_ids.append(int(post_id))
            if lang == "ru":
                m1 = \
                    "Выбрать причину для репорта:\n"\
                    "1.ЦП\n"\
                    "2.Ворованный контент\n"\
                    "3.Фейковый аккаунт или канал\n"\
                    "4.Порнография\n"\
                    "5.Спам\n"\
                    "6.Жестокость\n"\
                    "7.Другое\n"
            else:
                m1 = \
                    "Choose a reason of reporting:\n"\
                    "1.CP\n"\
                    "2.Stolen content\n"\
                    "3.Fake account or channel\n"\
                    "4.Pornography\n"\
                    "5.Spam\n"\
                    "6.Violence\n"\
                    "7.Other\n"
            print(m1)
            reason_num = int(input())-1
            if lang == "ru":
                comment = input("Напишите коммент о репорте: ")
                print("Отправка жалоб активирована...")
            else:
                print("Reports has been activated...")
                comment = input("Write comment about report: ")
            for acc in accs:
                try:
                    report.Report(
                        acc=acc,
                        post_ids=post_ids,
                        reason_num=reason_num,
                        comment=comment,
                        channel=channel
                    ).start()
                except:
                    pass
        elif a == 4:
            if lang == "ru":
                print("1.Добавить стикерпаки\n2.Убрать стикерпаки\n")
            else:
                print("1.Add stickerpacks\n2.Remove stickerpacks\n")
            m = int(input())
            if m == 1:
                if lang == "ru":
                    your_id = int(input("Введи свой айди в телеграм потом отправить стикер в чат с ботами: "))
                else:
                    your_id = int(input("Enter your telegram id then send sticker into the chat with bots: "))
                for acc in accs:
                    try:
                        addsticker.AddStickerpack(acc, your_id).start()
                    except:
                        pass
            if m == 2:
                for acc in accs:
                    try:
                        addsticker.RemoveStickerpacks(acc).start()
                    except:
                        pass
        elif a == 5:
            if lang == "ru":
                print(
                    '1.Установить био\n'
                    '2.Установить аватарку\n'
                    '3.Установить имя\n'
                    '4.Выйти со всех чатов и каналов\n'
                )
            else:
                print(
                    '1.Set bio\n'
                    '2.Set avatar\n'
                    '3.Set name\n'
                    '4.Leave from channels & chats\n'
                )
            a = int(input())
            if a == 1:
                if lang == "ru":
                    bio_text = input("Введи био: ")
                else:
                    bio_text = input("Enter bio: ")
                for acc in accs:
                    try:
                        additional.Bio(bio_text, acc).start()
                    except:
                        pass
            if a == 2:
                for acc in accs:
                    try:
                        additional.Avatar(acc).start()
                    except:
                        pass
            if a == 3:
                f = open("name.txt", encoding='utf-8', errors='ignore')
                namelist = f.read().split('\n')
                v = open("surname.txt", encoding='utf-8', errors='ignore')
                surnamelist = v.read().split('\n')
                f.close()
                v.close()
                for acc in accs:
                    try:
                        additional.CreateName(
                            acc,
                            namelist,
                            surnamelist
                        ).start()
                    except:
                        pass
            if a == 4:
                accs = os.listdir("tgaccs")
                x = 1
                if lang == "ru":
                    print("Выбрать аккаунт:")
                else:
                    print("Choose an account:")
                for acc in accs:
                    print(f"{x}. {acc}")
                    x += 1
                acc_input = int(input())-1
                if lang == "ru":
                    s = input("Уверены что надо удалить чаты? y/n\n")
                else:
                    s = input("Sure that you want to clear chats? y/n\n")
                if s == "y":
                    leave.LeaveChat(accs[acc_input]).start()
        elif a == 6:
            accs = os.listdir("tgaccs")
            if lang == "ru":
                a = input('Введи ссылку на пост: \n')
            else:
                a = input('Enter post link:\n ')
            b = a.split(',')
            ids = []
            private = False
            channel = b[0].split('/')[3]
            for x in b:
                x1 = x.split('/')
                if channel == "c":
                    private = True
                    ids.append(int(x1[5]))
                else:
                    ids.append(int(x1[4]))

            if private:
                channel = b[0].split('/')[4]
            for acc in accs:
                try:
                    view = see.Channel(acc, channel, ids, private)
                    view.start()
                except:
                    pass
        elif a == 7:
            if lang == "ru":
                poll_link = input("Вееди ссылку на сообщение с опросом: ")
            else:
                poll_link = input("Enter message link with poll: ")
            input_variants = input("Choose a variants:\nExmaple:1,2\n")

            variants = []
            for variant in input_variants.split(","):
                variants.append(str(int(variant)-1))
            private = False
            channel = poll_link.split('/')[3]
            x = poll_link.split('/')
            if channel == "c":
                private = True
                poll_id = int(x[5])
            else:
                poll_id = int(x[4])

            if private:
                channel = poll_link.split('/')[4]
            for acc in accs:
                try:
                    view = polls.Channel(acc, channel, poll_id, variants, private)
                    view.start()
                except:
                    pass

    except KeyboardInterrupt:
        break
    except ValueError:
        break
