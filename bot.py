from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from telethon.sync import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest

import asyncio
import config
import datetime
import re
import sqliter


client = TelegramClient('XXX', 13120094, '516784e5e2c31aae33fe55a07900b0e1')
client.connect()

sqliter.create_tables()

bot = Bot(token=config.token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
words = sqliter.get_words()
admins = sqliter.get_admins()

print('PARSER-bot successfully started!\nWaiting messages...')


def extract_arg(arg):
    return arg.split()[1]


@dp.message_handler(content_types=['text'])
async def main(message: types.Message):
    for i in admins:
        if str(message.chat.id) == str(i[0]):
            if message.text == '/help':
                await bot.send_message(message.chat.id, config.help_text, disable_web_page_preview=True)
            elif message.text == '/listwords':
                words_up = ''
                for i in words:
                    words_up += str(i[0]) + '\n'
                await bot.send_message(message.chat.id, words_up)
            elif '/addword' in message.text:
                try:
                    word = extract_arg(message.text)
                    sqliter.new_word(word)
                    await bot.send_message(message.chat.id, 'Новое слово для фильтра добавлено.')
                except Exception as e:
                    print(repr(e))
                    await bot.send_message(message.chat.id, 'В команде не указано слово.')
            elif '/delword' in message.text:
                try:
                    word = extract_arg(message.text)
                    sqliter.del_word(word)
                    await bot.send_message(message.chat.id, 'Слово для фильтра удалено из базы.')
                except Exception as e:
                    print(repr(e))
                    await bot.send_message(message.chat.id, 'В команде не указано слово или не найдено.')
            elif message.text == '/usrchats':
                listw = ''
                async for i in client.iter_dialogs():
                    listw += str(i.entity.username) + '\n'
                await bot.send_message(message.chat.id, listw)
            # elif message.text == '/namechats':
            #     listw = ''
            #     async for i in client.iter_dialogs():
            #         listw += str(i.entity.title) + '\n'
            #     await bot.send_message(message.chat.id, listw)
            elif '/addchat' in message.text:
                try:
                    userka = extract_arg(message.text)
                    if 't.me/' in userka:
                        if '+' in userka:
                            # https://t.me/+eKY-GeZRxpoxOWRi
                            userka = userka.split("+")[1]
                            await client(ImportChatInviteRequest(userka))
                        else:
                            userka = userka.split("t.me/")[1]
                            channel = await client.get_entity(userka)
                            await client(JoinChannelRequest(channel))
                        await bot.send_message(message.chat.id, 'Новый чат успешно добавлен на аккаунт.')
                    else:
                        await bot.send_message(message.chat.id, 'В команде не указана ссылка или не найдено!')
                except Exception as e:
                    print(repr(e))
                    await bot.send_message(message.chat.id, 'В команде не указана ссылка или не найдено.')
            elif '/delchat_n' in message.text:
                try:
                    name_chat = message.text[11:]
                    async for i in client.iter_dialogs():
                        if i.entity.title == name_chat:
                            await i.delete()
                    await bot.send_message(message.chat.id, 'Чат успешно удален с аккаунта.')
                except Exception as e:
                    print(repr(e))
                    await bot.send_message(message.chat.id, 'В команде не указано имя или не найдено.')
            elif '/delchat_u' in message.text:
                try:
                    user_chat = extract_arg(message.text)
                    async for i in client.iter_dialogs():
                        if i.entity.username == user_chat:
                            await i.delete()
                    await bot.send_message(message.chat.id, 'Чат успешно удален с аккаунта.')
                except Exception as e:
                    print(repr(e))
                    await bot.send_message(message.chat.id, 'В команде не указана ссылка или не найдено.')
            elif '/addadmin' in message.text:
                try:
                    user_id = extract_arg(message.text)
                    sqliter.add_admin(user_id)
                    await bot.send_message(message.chat.id, 'Администратор успешно добавлен в базу.')
                except Exception as e:
                    print(repr(e))
                    await bot.send_message(message.chat.id, 'В команде не указан айди.')
            elif '/deladmin' in message.text:
                if str(user_id) == str(message.chat.id):
                    await bot.send_message(message.chat.id, 'Нельзя удалить самого себя.')
                else:
                    try:
                        user_id = extract_arg(message.text)
                        sqliter.del_admin(user_id)
                        await bot.send_message(message.chat.id, 'Администратор успешно удален из базы.')
                    except Exception as e:
                        print(repr(e))
                        await bot.send_message(message.chat.id, 'В команде не указан айди.')
            elif message.text == '/getadmins':
                try:
                    for id_adm in admins:
                        await bot.send_message(message.chat.id, f'<a href="tg://user?id={id_adm[0]}">{id_adm[0]}</a>\n')
                except Exception as e:
                    print(repr(e))
                    await bot.send_message(message.chat.id, 'В команде не указан айди.')


@client.on(events.NewMessage())
async def normal_handler(event):
    info = event.message.to_dict()

    for i in words:
        if i[0] in re.sub('[^А-я]', ' ', info['message'].lower()).split():
            try:
                user_id = info['from_id']['user_id']
                lonami = await client.get_entity(user_id)
                channel_info = await client.get_entity(info['peer_id']['channel_id'])
                message_id = info['id']
                if channel_info.username is not None:
                    message_url = f't.me/{channel_info.username}/{message_id}'
                else:
                    message_url = 'Ссылка отсутствует (у чата)'

                all_name = str(lonami.first_name) + ' ' + str(lonami.last_name)
                username = str(lonami.username)

                date = info['date'] + datetime.timedelta(hours=3, minutes=0)
                answer = f'<b>📠 Название группы</b>: <i>{channel_info.title}</i>\n<b>' \
                         f'🔗 Ссылка на сообщение</b>: <i>{message_url}</i>\n<b>' \
                         f'⏳ Время отправки</b>: <i>{date}</i>\n' \
                         f'➖➖➖➖➖➖➖➖➖➖\n<b>' \
                         f'📩 Текст сообщения</b>: <i>' + \
                         info['message'] + f'</i>\n<b>' \
                         f'👨‍🦰 Имя пользователя</b>: <i>{all_name}</i>\n<b>' \
                         f'⛓ Никнейм</b>: <i>@{username}</i>\n<b>' \
                         f'🖱 UserID</b>: <i>{user_id}</i>'
                for id_adm in admins:
                    await bot.send_message(id_adm[0], answer, disable_web_page_preview=True)
                    print(f'[+] New message sent! Admin to - ' + str(id_adm[0]))
                break
            except Exception as e:
                print(repr(e))


async def on_startup(x):
    asyncio.create_task(client.run_until_disconnected())


executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
