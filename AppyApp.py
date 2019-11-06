#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Запись новых сообщений из чата в файл.

Version: 0.2
Created: 23/07/2019
Last modified: 25/07/2019
"""

import socks
import time
from telethon import TelegramClient, events, sync


def setup_client(proxy_ip, proxy_port):
    """
    Инициализация клиента.

    :param proxy_ip:
    :param proxy_port:
    :return:
    """
    # api_id = 
    # api_hash = ""
    proxy = (socks.SOCKS5, proxy_ip, proxy_port)
    client = TelegramClient('Common', api_id, api_hash, proxy=proxy)
    return client


def setup_events(client: TelegramClient, chats, file_obj):
    """
    Регистрация обработчиков событий.

    :param client:
    :param chats:
    :param file_obj:
    :return:
    """
    @client.on(events.NewMessage(chats=chats))
    async def normal_handler(event):
        """
        Обработка получения нового сообщения.

        :param event:
        :return:
        """
        # import telethon
        # telethon.types.Channel.
        # telethon.custom.Message.to_json()

        chat = await event.message.get_chat()
        message = event.message.to_dict()
        # Вывод сообщения
        print("\n\tNew message:")
        print(message)
        print(chat)
        print()
        print(message['date'].astimezone().strftime("%d-%m-%Y %H:%M:%S") +
              ' ' + chat.title + ' [' + chat.username + ']')
        print(message['message'])

        # user_id = message['from_id']
        # user = users.get(user_id)
        user_id = message.get('from_id')
        bot = '[BOT] ' if message.get('via_bot_id') is not None else ''
        print("\tFrom: " + bot + str(user_id) + '\n')

        # Запись сообщения в файл
        full_message = message['message'] + '\n'
        full_message += message['date'].astimezone().strftime("%d-%m-%Y %H:%M:%S")
        full_message += ' ' + chat.title + ' [' + chat.username + '] from ' + bot + str(user_id) + '\n'

        file_obj.write(full_message + '\n\n')
        file_obj.flush()

        # Запись сообщения в JSON файл
        with open('AppyApp_last_message.json', 'a') as fp:
            chat.to_json(fp)
            event.message.to_json(fp)
            fp.write('\n')


def main():
    # Список прокси
    proxies = [('193.124.178.45', 10080),  # ++
               ('212.22.92.121', 56342),  # ++
               ('145.239.81.69', 1080),
               ('95.110.230.142', 60892),
               ('94.156.129.13', 1080),  # ++++
               ('3.218.127.232', 1080),  # ++
               ('198.199.120.102', 1080)]
    # Список чатов
    chats = ["lentachold", "reddit", "yaplakal", "rhymestg"]

    # Соединение с Телеграмом через работающий прокси
    print()
    print(time.strftime("%H:%M:%S"), end=' ')
    print("Starting client...")
    for proxy in proxies:
        client = setup_client(proxy[0], proxy[1])
        try:
            client.start()
            print("Proxy {}:{} succeed".format(proxy[0], proxy[1]))
            break
        except ConnectionError:
            print("Proxy {}:{} failed".format(proxy[0], proxy[1]))
    else:
        print("Connection failed")
        return
    print(time.strftime("%H:%M:%S"), end=' ')
    print("Client started...")

    # Файл для записи сообщений
    f = open('AppyApp_messages.txt', 'a')

    setup_events(client, chats, f)

    # Вывод последнего сообщения первого чата
    print("\n\tLast message:")
    messages = client.get_messages(chats[0])
    for message in messages:
        print(message.date.astimezone().strftime("%d-%m-%Y %H:%M:%S") +
              ' ' + message.chat.title + ' [' + message.chat.username + ']')
        print(message.text)
        # print(message.chat)

    # users = {}
    # for user in client.iter_participants(chats):
    #     last_name = user.last_name if user.last_name else ''
    #     username = user.username if user.username else ''
    #     user_s = user.first_name + " | " + last_name + " | " + username + " | " + user.phone
    #     if user.bot:
    #         user_s = "[BOT] " + user_s
    #     users[user.id] = user_s
    #
    # with open('AppyApp_users.txt', 'w') as file:
    #     file.write("Users of {}:\n".format(chats))
    #     file.writelines(users)

    # Основной цикл
    client.run_until_disconnected()

    # async def input_loop():
    #     nonlocal stop
    #     input_string = input()
    #     if input_string == 'stop':
    #         stop = True
    #
    # input_loop()
    # stop = False
    # while not stop:
    #     pass
    client.disconnect()
    print(time.strftime("%H:%M:%S"), end=' ')
    print("Client disconnected")

    f.close()


if __name__ == '__main__':
    __time_start = time.perf_counter()
    main()
    __time_delta = time.perf_counter() - __time_start
    __TIMES = (('d', 24 * 60 * 60), ('h', 60 * 60), ('m', 60), ('input_string', 1))
    __times = ''
    for __idx in range(len(__TIMES) - 1):
        __t, __time_delta = divmod(__time_delta, __TIMES[__idx][1])
        if __t > 0:
            __times += "{} {} ".format(int(__t), __TIMES[__idx][0])
    __times += "{:.3} {}".format(__time_delta, __TIMES[~0][0])
    print("\n[Finished in {}]".format(__times))
