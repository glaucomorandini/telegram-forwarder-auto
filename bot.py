#    Copyright (c) 2021 Ayush
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
#    License can be found in < https://github.com/Ayush7445/telegram-auto_forwarder/blob/main/License > .

from telethon import TelegramClient, events
from decouple import config
import logging
from telethon.sessions import StringSession

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

print("Starting...")

# Basics
APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
SESSION = config("SESSION")
FROM_ = config("FROM_CHANNEL")
TO_ = config("TO_CHANNEL")

FROM = [int(i) for i in FROM_.split()]
TO = [int(i) for i in TO_.split()]

try:
    client = TelegramClient(StringSession(SESSION), APP_ID, API_HASH)
    client.start()
except Exception as ap:
    print(f"ERROR - {ap}")
    exit(1)

@client.on(events.NewMessage(incoming=True, chats=FROM))
async def sender_message(event):
    async with client:
        print('--- client')
        try:
            # # Does it have a username? Use it!
            # entity = await client.get_entity(username)

            # Do you have a conversation open with them? Get dialogs.
            await client.get_dialogs()

            # Are they participant of some group? Get them.
            await client.get_participants('glaucomorandini')

            # Is the entity the original sender of a forwarded message? Get it.
            await client.get_messages('glaucomorandini', 100)

            for i in TO:
                await client.send_message(
                    i,
                    event.message
                )

                entity = await client.get_entity(i)
                print(entity)

        except Exception as e:
            print('cannot fetch user')
            print(e)

print("Bot has started.")
client.run_until_disconnected()
