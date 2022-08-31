# import sqlite3, config, requests
# from datetime import datetime
# path_db = 'database.db'
#
# def get_admins():
#     with sqlite3.connect(config.path_db) as c:
#         return c.execute("SELECT * FROM admins").fetchall()
#
# for i in get_admins():
#     print(i[0])

# print(get_admins())

import re

import sqliter
import time
start_time = time.time()

words = sqliter.get_words()

title = 1
message_url = 2
date = time.time()
all_name = 'Denis'
username = 'DMD'
user_id = 123456
# with open('message.txt', 'r', encoding='utf-8') as f:
#     s1 = re.sub('[^А-я]', ' ', f.read()).strip()

s = f'<b>📠 Название группы</b>: <i>{title}</i>\n<b>' \
                         f'🔗 Ссылка на сообщение</b>: <i>{message_url}</i>\n<b>' \
                         f'⏳ Время отправки</b>: <i>{date}</i>\n➖➖➖➖➖➖➖➖➖➖\n<b>' \
                         f'📩 Текст сообщения</b>: <i>' + \
                         f'👨‍🦰 Имя пользователя</b>: <i>{all_name}</i>\n<b>' \
                         f'⛓ Никнейм</b>: <i>@{username}</i>\n<b>🖱 UserID</b>: <i>{user_id}</i>'
start_time = time.time()
# print(re.sub('[^А-я]', ' ', s))
# res = re.sub('[^А-я]', ' ', s).split()
print(s)
# print(re.sub('[^А-я]', ' ', s.lower()).split())
# for i in words:
#     print(i[0])
#     if i[0] in re.sub('[^А-я]', ' ', s).split():
# #     # print(i)
#         print('Нашел')




print("--- %s seconds ---" % (time.time() - start_time))

token = '2140516643:AAEUVVDTalAGyUHqpp_WBlgXwvj8FkbLO-Q'
api_id = 9042257
api_hash = '8cef84a50841072a43d246dc8d76c911'
