import telebot
from telebot import types
from random import choice
from datetime import date
import speech_recognition as sr




language='ru_RU'
r = sr.Recognizer()
bot = telebot.TeleBot('#')
tail=' '
todo = { }


daysofmonth= {'Январь':31, 'Февраль':28, 'Март':31, 'Апрель':30, 'Май':31, 'Июнь':30, 'Июль':31, 'Август':31,\
              'Сентябрь':30, 'Октябрь':31, 'Ноябрь':30, 'Декабрь':31}
daysofmonthvisokos={'Январь':31, 'Февраль':29, 'Март':31, 'Апрель':30, 'Май':31, 'Июнь':30, 'Июль':31, 'Август':31,\
              'Сентябрь':30, 'Октябрь':31, 'Ноябрь':30, 'Декабрь':31}
RANDOM_TASKS = ['Заняться спортом', 'Написать программу на Python', 'Почитать книгу', 'Медитация']

HELP = '''
Список доступных команд:
* print  - напечать все задачи на заданную дату
* todo - добавить задачу
* random - добавить на сегодня случайную задачу
* help - Напечатать help
'''
def add_todo(result, tail):
    if todo.get(result) is not None:
        todo[result].append(tail)
    else:
        todo[result] = [tail]

@bot.message_handler(commands=["start"])
def start_message(message):
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button2 = types.KeyboardButton('Случайная задача на сегодня')
    button3 = types.KeyboardButton('Выберите дату для просмотра задач')
    buttons.add(button2, button3)
    bot.send_message(message.chat.id, text="Добро пожаловать", reply_markup=buttons)


def years():
    buttons = types.InlineKeyboardMarkup(row_width=2)
    key3 = types.InlineKeyboardButton(text='Текущий год', callback_data='year')
    key4 = types.InlineKeyboardButton(text='Следующий год', callback_data='year2')
    buttons.add(key3, key4)
    return buttons
def mauth():
    buttons = types.InlineKeyboardMarkup()
    mauth1=[]
    for key in daysofmonth:
        mauth1.append(key)
    n = 2
    but1 = [mauth1[idx:idx + n] for idx in range(0, len(mauth1), n)]
    for i in range(len(but1)):
        key1 = types.InlineKeyboardButton(text=but1[i][0], callback_data='mauth'+str(but1[i][0]))
        key2 = types.InlineKeyboardButton(text=but1[i][1], callback_data='mauth'+str(but1[i][1]))
        buttons.add(key1,key2)
    return buttons


def mauthV():
    buttons = types.InlineKeyboardMarkup()
    mauth1=[]
    for key in daysofmonthvisokos:
        mauth1.append(key)
    n = 2
    but1 = [mauth1[idx:idx + n] for idx in range(0, len(mauth1), n)]
    for i in range(len(but1)):
        key1 = types.InlineKeyboardButton(text=but1[i][0], callback_data='mauthV'+str(but1[i][0]))
        key2 = types.InlineKeyboardButton(text=but1[i][1], callback_data='mauthV'+str(but1[i][1]))
        buttons.add(key1,key2)
    return buttons


def day(key):
    buttons = types.InlineKeyboardMarkup()
    prob=[]
    for daite in range(1, (daysofmonth[key] + 1)):
        dayy=str(daite)
        prob.append(types.InlineKeyboardButton(text=dayy, callback_data='day'+dayy))
    buttons.add(*prob)
    return buttons


def dayV(key):
    buttons = types.InlineKeyboardMarkup()
    prob=[]
    for daiteV in range(1, (daysofmonthvisokos[key] + 1)):
        dayyV=str(daiteV)
        prob.append(types.InlineKeyboardButton(text=dayyV, callback_data='dayV'+dayyV))
    buttons.add(*prob)
    return buttons

def todos():
    buttons = types.InlineKeyboardMarkup()
    for keyy in todo:
        keyy = str(keyy)
        keys = types.InlineKeyboardButton(text=keyy, callback_data='todos' + keyy)
        buttons.add(keys)
    return buttons

def todosday(keyy):
    buttons = types.InlineKeyboardMarkup(row_width=2)
    for keyyw in todo:
        keyy = str(keyy)
        keys1 = types.InlineKeyboardButton(text=(("\N{calendar}")+'Перенести '), callback_data='datta'+keyy)
        keys2 = types.InlineKeyboardButton(text=(("\N{check mark}")+'Выполнено'), callback_data='dalete1'+keyy)
        keys3 = types.InlineKeyboardButton(text=(("\N{cross mark}")+'Удалить'), callback_data='dalete' + keyy)
        buttons.add(keys1,keys2, keys3)
        return buttons

def todosdayi(keyy,i):
    buttons = types.InlineKeyboardMarkup(row_width=2)
    for keyyz in todo:
        if keyyz==keyy:
            i=int(i)
            re=todo[keyy][i]
            keyy = str(keyy)
            keys1 = types.InlineKeyboardButton(text=(("\N{calendar}")+'Перенести '), callback_data='datta' + re)
            keys2 = types.InlineKeyboardButton(text=("\N{check mark}")+'Выполнено', callback_data='dalete1' + re)
            keys3 = types.InlineKeyboardButton(text=("\N{cross mark}")+'Удалить', callback_data='dalete' + re)
            buttons.add(keys1, keys2, keys3)
    return buttons


@bot.message_handler(content_types=['text'])
def answer(message):
    try:
        if message.text == 'Случайная задача на сегодня':
            buttons32 = types.InlineKeyboardMarkup(row_width=1)
            tailt = choice(RANDOM_TASKS)
            resu=date.today()
            bot.send_message(message.chat.id, text=tailt , reply_markup=buttons32)
            result=''.join(str(resu))
            add_todo(result, tailt)

        elif message.text == 'Выберите дату для просмотра задач':
            if len(todo)==0:
                bot.send_message(message.chat.id, text='Нет дат для выбора ')
            elif len(todo)>=1:
                buttons=todos()
                bot.send_message(message.chat.id, 'Выберите', reply_markup=buttons)

        else:
            buttons32 = types.InlineKeyboardMarkup(row_width=2)
            key2 = types.InlineKeyboardButton(text='Выбрать дату', callback_data='datta')
            buttons32.add(key2)
            global tail
            tail = message.text
            bot.send_message(message.chat.id, text=('Установите дату для задачи  ' + message.text), reply_markup=buttons32)


    except Exception as e:
        print(repr(e))


dayta = []
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        n = 0
        v = 0
        if call.message:
            global tail

            if call.data == 'datta':
                bot.send_message(call.message.chat.id, 'Выберите год', reply_markup=years())
                bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                              message_id=call.message.message_id, reply_markup=None)
                bot.delete_message(call.message.chat.id, call.message.message_id)

            elif call.data == 'year2':
                year = date.today().year+1
                dayta.append(str(year))
                if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
                    bot.send_message(call.message.chat.id, 'Выберите месяц', reply_markup=mauthV())
                else:
                    bot.send_message(call.message.chat.id, 'Выберите месяц', reply_markup=mauth())
                bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                              message_id=call.message.message_id, reply_markup=None)
                bot.delete_message(call.message.chat.id, call.message.message_id)

            elif call.data == 'year':
                year = date.today().year
                dayta.append(str(year))
                if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
                    bot.send_message(call.message.chat.id, 'Выберите месяц', reply_markup=mauthV())
                else:
                    bot.send_message(call.message.chat.id, 'Выберите месяц', reply_markup=mauth())
                bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                              message_id=call.message.message_id, reply_markup=None)
                bot.delete_message(call.message.chat.id, call.message.message_id)


            for key in daysofmonthvisokos:
                n += 1
                if call.data == 'mauthV' + key:
                    if n < 10:
                        dayta.append('0' + str(n))
                    else:
                        dayta.append(str(n))
                    bot.send_message(call.message.chat.id, 'Выберите день', reply_markup=dayV(key))
                    bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                                  message_id=call.message.message_id, reply_markup=None)
                    bot.delete_message(call.message.chat.id, call.message.message_id)

            for dayyV in range(1, (daysofmonthvisokos[key] + 1)):
                dayyV = str(dayyV)
                if call.data == 'dayV' + dayyV:
                    dayta.append(dayyV)
                    result = '-'.join(dayta)
                    res = reversed(dayta)
                    add_todo(result, tail)
                    bot.send_message(call.message.chat.id,
                                     text='задача ' + tail + ' установлена на ' + ' '.join(res))
                    dayta.clear()
                    bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                                  message_id=call.message.message_id, reply_markup=None)
                    bot.delete_message(call.message.chat.id, call.message.message_id)

            for i in daysofmonth:
                v += 1
                if call.data == 'mauth' + i:
                    if v < 10:
                        dayta.append('0' + str(v))
                    else:
                        dayta.append(str(v))
                    bot.send_message(call.message.chat.id, 'Выберите день', reply_markup=day(key))
                    bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                                  message_id=call.message.message_id, reply_markup=None)
                    bot.delete_message(call.message.chat.id, call.message.message_id)

            for dayy in range(1, (daysofmonth[key] + 1)):
                dayy = str(dayy)
                if call.data == 'day' + dayy:
                    dayta.append(dayy)
                    result = '-'.join(dayta)
                    res = reversed(dayta)
                    add_todo(result, tail)
                    bot.send_message(call.message.chat.id,
                                     text='задача ' + tail +' установлена на ' + ' '.join(res))
                    dayta.clear()
                    bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                                  message_id=call.message.message_id, reply_markup=None)
                    bot.delete_message(call.message.chat.id, call.message.message_id)

            for keyy in todo:
                keyy = str(keyy)
                if call.data == 'todos' + keyy:
                    bot.send_message(call.message.chat.id, 'Задачи на: ' + keyy)
                    if len(todo[keyy]) == 1:
                        bot.send_message(call.message.chat.id, todo[keyy], reply_markup=todosday(keyy))
                    elif len(todo[keyy]) >= 2:
                        for w in range(0, len(todo[keyy])):
                            texte = todo[keyy][w]
                            texte = str(texte)
                            i = str(w)
                            bot.send_message(call.message.chat.id, texte, reply_markup=todosdayi(keyy, i))
                    bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                                  message_id=call.message.message_id, reply_markup=None)
                    bot.delete_message(call.message.chat.id, call.message.message_id)

            for kluch in todo:
                keyy = str(kluch)
                if call.data == 'dalete'+keyy:
                    bot.send_message(call.message.chat.id, 'Удалено!')
                    del todo[kluch]
                    bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                                  message_id=call.message.message_id, reply_markup=None)
                    bot.delete_message(call.message.chat.id, call.message.message_id)


            for kluch in todo:
                keyy = str(kluch)
                if call.data == 'dalete1'+keyy:
                    bot.send_message(call.message.chat.id, 'Выполнено!')
                    del todo[kluch]
                    bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                                  message_id=call.message.message_id, reply_markup=None)
                    bot.delete_message(call.message.chat.id, call.message.message_id)

            for keyyt in todo:
                keyyt = str(keyyt)
                if call.data == 'datta' + keyy:
                    if keyy == keyyt:
                        buttons3 = types.InlineKeyboardMarkup(row_width=2)
                        key2 = types.InlineKeyboardButton(text='Выбрать дату', callback_data='datta')
                        buttons3.add(key2)
                        tail2 = todo.pop(keyy)
                        tail3 = str(tail2)
                        tail = tail3[2:len(tail3) - 2]
                        bot.send_message(call.message.chat.id, text=('Установите дату для задачи  ' + tail),
                                         reply_markup=buttons3)
                        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                                      message_id=call.message.message_id, reply_markup=None)
                        bot.delete_message(call.message.chat.id, call.message.message_id)
                        del todo[keyyt]
                        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                                      message_id=call.message.message_id, reply_markup=None)
                        bot.delete_message(call.message.chat.id, call.message.message_id)


            for keyyl in todo:
                for i in range(0, len(todo[keyyl])):
                    re = todo[keyyl][i]
                    if call.data == 'dalete1'+re:
                        bot.send_message(call.message.chat.id, 'Выполнено!')
                        del todo[keyyl][i]
                        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                                      message_id=call.message.message_id, reply_markup=None)
                        bot.delete_message(call.message.chat.id, call.message.message_id)

            for keyyl in todo:
                for i in range(0, len(todo[keyyl])):
                    re = todo[keyyl][i]
                    if call.data == 'dalete'+re:
                        bot.send_message(call.message.chat.id, 'Удалено!')
                        del todo[keyyl][i]

                        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                                      message_id=call.message.message_id, reply_markup=None)
                        bot.delete_message(call.message.chat.id, call.message.message_id)


            for keyyd in todo:
                for i in range(0, len(todo[keyyd])):
                    re = todo[keyyd][i]
                    if call.data == 'datta' + re:
                        buttons3 = types.InlineKeyboardMarkup(row_width=2)
                        key2 = types.InlineKeyboardButton(text='Выбрать дату', callback_data='datta')
                        buttons3.add(key2)
                        tail = re
                        bot.send_message(call.message.chat.id, text=('Установите дату для задачи  ' + tail),
                                         reply_markup=buttons3)
                        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                                      message_id=call.message.message_id, reply_markup=None)
                        bot.delete_message(call.message.chat.id, call.message.message_id)
                        del todo[keyyd][i]
                bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                              message_id=call.message.message_id, reply_markup=None)
                bot.delete_message(call.message.chat.id, call.message.message_id)


    except Exception as e:
        print(repr(e))

print(dayta)


bot.polling()
