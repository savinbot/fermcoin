# -*- coding: utf-8 -*-
import telebot
import cherrypy
import time
from telebot import types
from datetime import date, datetime
from sql_queries import *
import botan
import threading as th
from message_key import *


botan_key = 'BOTAN_KEY'
token = '604698563:AAGPXjamODcRav7wnweEcxcraHpIMnGFVts'
bot = telebot.TeleBot(token)


def timer():
    while True:
        now = datetime.now()
        if now.hour == 0:
            update_coin()
            time.sleep(3600)
        time.sleep(10)
t = th.Thread(target=timer, daemon=True)
t.start()


# keyboards
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
keyboard.add(*[types.KeyboardButton(name) for name in ['✅ Статистика', '🔆 Получить XBC', '💸 Как заработать', '💡 Связь с нами']])

keyboard_lk = types.InlineKeyboardMarkup()
btn_lk = types.InlineKeyboardButton(text="💵 Вывод", callback_data="money_exit")
keyboard_lk.add(btn_lk)

keyboard_exit = types.InlineKeyboardMarkup()
btc_exit = types.InlineKeyboardButton(text="📌 Создать заявку", callback_data="request_exit")
keyboard_exit.add(btc_exit)

keyboard_qiwi = types.InlineKeyboardMarkup()
ok = types.InlineKeyboardButton(text="✅ Ok", callback_data="ok_qiwi")
not_ok = types.InlineKeyboardButton(text="❌ Not Ok", callback_data="not_ok_qiwi")
keyboard_qiwi.add(ok, not_ok)


def no_xbc_users():
    rows = get_no_xbc()
    error = 0
    luck = 0
    for i in range(0, len(rows)):
        try:
            bot.send_message(rows[i][1], no_xbc_msg(rows[i][1]), parse_mode='Html', reply_markup=keyboard)
            luck = luck + 1
        except:
            error = error + 1
    bot.send_message(447583391, 'Luck: ' + str(luck) + '\nError: ' + str(error), parse_mode='Html', reply_markup=keyboard)


def qiwi_number(message):
    if message.text.isdigit():
        bot.send_message(message.chat.id, '📈 <i>Вывод на</i> <b>Qiwi</b> <i>кошелек</i> 📉\n+' + str(message.text), parse_mode='Html', reply_markup=keyboard_qiwi)
        set_qiwi(message.chat.id, message.text)
    elif message.text == '💸 Как заработать' or message.text == '💡 Коммерция' or message.text == '✅ Статистика' or message.text == '🔆 Получить XBC':
        key(message)
    else:
        sent = bot.send_message(message.chat.id, '😔 <b>Неверный ввод</b>\nПопробуйте еще раз...', parse_mode="Html")
        bot.register_next_step_handler(sent, qiwi_number)


@bot.message_handler(commands=["start"])
def start(message):
    if (message.text[7:].isdigit()):
        add_user_ref(message.chat.id, message.text[7:])
    else:
        add_user(message.chat.id)
    bot.send_message(message.chat.id, main_msg(message.chat.id, message.chat.first_name), parse_mode='Html', reply_markup=keyboard)
    botan.track(botan_key, message.chat.id, message, 'start')


@bot.message_handler(content_types=["text"])
def key(message):
    if message.text == '💸 Как заработать':
        bot.send_message(message.chat.id, main_msg(message.chat.id, message.chat.first_name), parse_mode='Html', reply_markup=keyboard)
        botan.track(botan_key, message.chat.id, message, 'how_money')
    elif message.text == '💡 Связь с нами':
        bot.send_message(message.chat.id, commerce_msg(), parse_mode='Html',  reply_markup=keyboard)
        botan.track(botan_key, message.chat.id, message, 'commerce')
    elif message.text == '✅ Статистика':
        bot.send_message(message.chat.id, stats_msg(message.chat.id), parse_mode='Html', reply_markup=keyboard_lk)
        botan.track(botan_key, message.chat.id, message, 'stats')
    elif message.text == '🔆 Получить XBC':
        botan.track(botan_key, message.chat.id, message, 'free_xbc')
        user = get_user(message.chat.id)
        if user[7] == 0 or user[7] == None:
            set_coin(message.chat.id)
            bot.send_message(message.chat.id, pay_true_msg(message.chat.id), parse_mode='Html', reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, pay_false_msg(message.chat.id), parse_mode='Html', reply_markup=keyboard)
    elif message.text == '!' and message.chat.id == 447583391:
        no_xbc_users()
    elif message.text == '?' and message.chat.id == 447583391:
        bot.send_message(447583391, str(len(get_all())))


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "money_exit":
            user = get_user(call.message.chat.id)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=stats_msg(call.message.chat.id) + '\n\n<b>💵 Вывод доступен на Qiwi</b>\n\n'
                                  'Минимальная сумма вывода: <code>30 XBC</code>\nУ вас на счету: <code>' + str(round(user[4], 2)) + ' XBC</code>',
                                  parse_mode='Html')
            if user[4] >= 30:
                bot.send_message(call.message.chat.id, '👇 <i>Создание заявки на вывод средств</i> 👇',
                                 parse_mode="Html", reply_markup=keyboard_exit)
        elif call.data == 'request_exit':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='<b>📌 Заявка на вывод</b>', parse_mode='Html')
            sent = bot.send_message(call.message.chat.id,
                                    'Введите свой номер <b>Qiwi</b> кошелька без знака <b>+</b>\n',
                                    parse_mode='Html')
            bot.register_next_step_handler(sent, qiwi_number)
        elif call.data == 'ok_qiwi':
            user = get_user(call.message.chat.id)
            qiwi_num = '+' + str(user[6])
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🚀 Ваша заявка создана\nОжидайте вывод на номер ' + qiwi_num, parse_mode='Html')
            bot.send_message(447583391, feedback_msg(user), parse_mode='Html')
        elif call.data == 'not_ok_qiwi':
            sent = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                         text='👉 Повторите ввод Qiwi кошелька...', parse_mode='Html')
            bot.register_next_step_handler(sent, qiwi_number)

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        length = int(cherrypy.request.headers['content-length'])
        json_string = cherrypy.request.body.read(length).decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''

if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 7771,
        'engine.autoreload.on': True,
    })
    cherrypy.quickstart(WebhookServer(), '/', {'/': {}})
