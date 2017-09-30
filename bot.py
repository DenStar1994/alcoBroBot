# -*- coding: utf-8 -*-


import telebot
from telebot import types
import time
import sqlite3
import consts
import re
from SQLighter import SQLighter
from keyboards import keyboards



knownUsers = []
userStep = {}

commands = {
    'start': 'Запусти меня',
    'help': 'Информация о командах',
    'buy': 'Делать покупки',
    'closeOrder': 'Завершить заказ'
}

id_order = int(SQLighter.get_max_id_order()) + 1;


def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0


# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)


bot = telebot.TeleBot(consts.token)
bot.set_update_listener(listener)  # register listener


@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:
        knownUsers.append(cid)
        userStep[cid] = 0
        bot.send_message(cid, "Привет, дружище! Хочешь выпить, но уже не продают? Могу помочь;)")
        bot.send_message(cid, "Жми /buy")
        command_help(m)
    else:
        bot.send_message(cid, "Опа, здарова! Ну ты знаешь что делать, тыкай /buy")


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "Если кто-то сюда заходит, то вот мои команды: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)


@bot.message_handler(regexp="(Добавить в заказ)|(Делать покупки)")
@bot.message_handler(commands=['buy'])
def command_buy(m):
    cid = m.chat.id
    bot.send_message(cid, "Что будешь пить? Гляди что у меня есть.", reply_markup=keyboards.alcoSelect)
    userStep[cid] = consts.select_alco_type_step

@bot.message_handler(regexp='Закончить заказ')
@bot.message_handler(commands=['closeOrder'])
def command_close(m):
    cid = m.chat.id
    text = m.text
    print(SQLighter.if_known_client(cid))
    if SQLighter.if_known_client(cid) == 1:
        bot.send_message(cid, "Не в первый раз, да?) "
                              "" +SQLighter.get_client_tel(cid)+" - твой номер?", reply_markup=keyboards.verify)
        userStep[cid] = consts.confirm_tel
    else:
        bot.send_message(cid, "Теперь мне нужна твоя одежда и мотоцикл")
        bot.send_message(cid, "Тьфу, это с другой работы, с тебя номер телефона и адрес")
        bot.send_message(cid, "Вводи телефон")
        userStep[cid] = consts.new_client

@bot.message_handler(regexp='Отменить заказ')
@bot.message_handler(commands=['rejectOrder'])
def command_creject(m):
    cid = m.chat.id
    text = m.text
    SQLighter.confirm_order(0, cid)
    SQLighter.total_confirm(0, cid)
    bot.send_message(cid, "Все отменил, давай жми /buy или кнопку и делай покупки", reply_markup=keyboards.command)
    userStep[cid] = consts.null_step

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == consts.confirm_tel)
def confirm_tel(m):
    cid = m.chat.id
    text = m.text
    if text == 'Да':
        bot.send_message(cid, SQLighter.get_client_addr(cid)+" - твой адрес?", reply_markup=keyboards.verify)
        userStep[cid] = consts.confirm_addr
    elif text == 'Нет':
        bot.send_message(cid, "Введи свой")
        userStep[cid] = consts.new_tel
    else:
        bot.send_message(cid, "Выбери вариант")

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == consts.confirm_addr)
def confirm_addr(m):
    cid = m.chat.id
    text = m.text
    if text == 'Да':
        # формируем итоговый заказ
        i = 0
        pos = ''
        while i < len(list(SQLighter.get_order_pos(cid))):
            item = str(SQLighter.get_order_pos(cid)[i]).replace('(\'', '').replace('\',)', '')  # удаляем скобки
            pos = pos + ', ' + item
            i = i + 1
        #bot.send_message(363822878, "Там " + m.chat.first_name + " заказал "+ pos[2:pos.__len__()]+" на сумму "+SQLighter.get_total_sum(cid))
        #bot.send_message(91675058, "Там " + m.chat.first_name + " заказал "+ pos[2:pos.__len__()]+" на сумму "+SQLighter.get_total_sum(cid))
        #bot.send_message(136356612, "Там " + m.chat.first_name + " заказал "+ pos[2:pos.__len__()]+" на сумму "+SQLighter.get_total_sum(cid))

        bot.send_message(cid, "Твой заказ " + pos[2:pos.__len__()]+" сумма "+SQLighter.get_total_sum(cid))
        bot.send_message(cid,"Все верно?", reply_markup=keyboards.confirm_order)
        userStep[cid] = consts.confirm_order
    elif text == 'Нет':
        bot.send_message(cid, "Введи свой")
        userStep[cid] = consts.new_addr
    else:
        bot.send_message(cid, "Выбери вариант")


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == consts.confirm_order)
def confirm_addr(m):
    cid = m.chat.id
    text = m.text
    if text == 'Да':
        # формируем итоговый заказ
        i = 0
        pos = ''
        while i < len(list(SQLighter.get_order_pos(cid))):
            item = str(SQLighter.get_order_pos(cid)[i]).replace('(\'', '').replace('\',)', '')  # удаляем скобки
            pos = pos + ', ' + item
            i = i + 1
        bot.send_message(363822878, "Там " + m.chat.first_name + " заказал " + pos[
                                                                               2:pos.__len__()] + " на сумму " + SQLighter.get_total_sum(
            cid))
        bot.send_message(91675058, "Там " + m.chat.first_name + " заказал " + pos[
                                                                              2:pos.__len__()] + " на сумму " + SQLighter.get_total_sum(
            cid))
        bot.send_message(136356612, "Там " + m.chat.first_name + " заказал " + pos[
                                                                               2:pos.__len__()] + " на сумму " + SQLighter.get_total_sum(
            cid))
        SQLighter.total_confirm(1,cid)
        bot.send_message(cid,
                         "Я тебя понял, теперь жди звонка, мои ребята метнутся и все принесут. Будь осторожен - это серьезные люди (нет)")
        userStep[cid] = 0
    elif text == 'Поменять адрес':
        bot.send_message(cid, "Вводи адрес")
        userStep[cid] = consts.new_addr
    elif text == 'Поменять телефон':
        bot.send_message(cid, "Вводи телефон")
        userStep[cid] = consts.only_tel
    elif text == 'Я только посмотреть хотел':
        bot.send_message(cid, "Ок, все отменяем", reply_markup=keyboards.command)
        SQLighter.total_confirm(0, cid)
        userStep[cid] = 0
    else:
        bot.send_message(cid, "Выбери вариант")


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == consts.new_client)
def get_tel(m):
    cid = m.chat.id
    n_tel = m.text
    tel = re.compile("^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$")
    if re.match(tel,n_tel) is not None:
        SQLighter.insert_client(id_order, n_tel, cid, m.chat.first_name)
        bot.send_message(cid, "И адрес")
        userStep[cid] = consts.new_addr
    else:
        bot.send_message(cid, "Вводи нормально")

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == consts.new_tel)
def get_tel(m):
    cid = m.chat.id
    n_tel = m.text
    tel = re.compile("^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$")
    if re.match(tel,n_tel) is not None:
        SQLighter.update_client_tel(cid, n_tel)
        bot.send_message(cid, SQLighter.get_client_addr(cid) + " - твой адрес?", reply_markup=keyboards.verify)
        userStep[cid] = consts.confirm_addr
    else:
        bot.send_message(cid, "Вводи нормально")

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == consts.only_tel)
def get_tele(m):
    cid = m.chat.id
    n_tel = m.text
    print('hello1')
    tel = re.compile("^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$")
    if re.match(tel,n_tel) is not None:
        SQLighter.update_client_tel(cid, n_tel)
        # формируем итоговый заказ
        i = 0
        pos = ''
        while i < len(list(SQLighter.get_order_pos(cid))):
            item = str(SQLighter.get_order_pos(cid)[i]).replace('(\'', '').replace('\',)', '')  # удаляем скобки
            pos = pos + ', ' + item
            i += 1
        bot.send_message(cid, "Твой заказ " + pos[2:pos.__len__()] + " сумма " + SQLighter.get_total_sum(cid))
        bot.send_message(cid, "Все верно?", reply_markup=keyboards.confirm_order)
        userStep[cid] = consts.confirm_order
    else:
        bot.send_message(cid, "Вводи нормально")

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == consts.new_addr)
def get_addr(m):
    cid = m.chat.id
    v_addr = m.text
    SQLighter.update_client_addr(cid, v_addr)
    i = 0
    pos = ''
    while i < len(list(SQLighter.get_order_pos(cid))):
        item = str(SQLighter.get_order_pos(cid)[i]).replace('(\'', '').replace('\',)', '')  # удаляем скобки
        pos = pos + ', ' + item
        i = i + 1
    bot.send_message(cid, "Твой заказ " + pos[2:pos.__len__()] + " сумма " + SQLighter.get_total_sum(cid))
    bot.send_message(cid, "Все верно?", reply_markup=keyboards.confirm_order)
    userStep[cid] = consts.confirm_order
id_order = id_order+1



@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == consts.select_alco_type_step)
def select_alco(m):
    cid = m.chat.id
    text = m.text
    bot.send_chat_action(cid, 'typing')
    if text == "Водка":
        bot.send_message(cid, "Шутейка про водку и алкашей, смотри че почем.", reply_markup=keyboards.vodkaKey)
        userStep[cid] = consts.select_alco_item_step
    elif text == "Ягерь":
        bot.send_message(cid, "Шутейка про ягерь и какой он охуенный, смотри че почем.", reply_markup=keyboards.likerKey)
        print(id_order)
        userStep[cid] = consts.select_alco_item_step
    elif text == "Пиво":
        bot.send_message(cid, "Шутейка про пиво и пузан, смотри че почем.", reply_markup=keyboards.beerKey)
        userStep[cid] = consts.select_alco_item_step
    elif text == "Вино":
        bot.send_message(cid, "Шутейка про вино и романтику, смотри че почем.", reply_markup=keyboards.vineKey)
        userStep[cid] = consts.select_alco_item_step
    elif text == "Ром":
        bot.send_message(cid, "Шутейка про ром и пиратов, смотри че почем.", reply_markup=keyboards.romKey)
        userStep[cid] = consts.select_alco_item_step
    elif text == "Виски":
        bot.send_message(cid, "Шутейка про виски и ковбоев, смотри че почем.", reply_markup=keyboards.wiskeyKey)
        userStep[cid] = consts.select_alco_item_step
    elif text == "Джин":
        bot.send_message(cid, "Шутейка про вологодский джин, смотри че почем.", reply_markup=keyboards.ginKey)
        userStep[cid] = consts.select_alco_item_step
    elif text == "Абсент":
        bot.send_message(cid, "Шутейка про крепость, смотри че почем.", reply_markup=keyboards.absentKey)
        userStep[cid] = consts.select_alco_item_step
    elif text == "Текилла":
        bot.send_message(cid, "Шутейка про мексиканскую вечеринку, смотри че почем.", reply_markup=keyboards.tekillaKey)
        userStep[cid] = consts.select_alco_item_step
    else:
        bot.send_message(cid, "Такого нет, братан")
        bot.send_message(cid, "Вон же кнопки, че ты")




@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == consts.select_alco_item_step)
def select_cnt(m):
    print('select_cnt')
    cid = m.chat.id
    text = m.text
    bot.send_chat_action(cid, 'typing')
    #проверим, что чувак выбрал что-то из меню он мог ввести чт0-то, чего нет в кнопках - пофиг, пройдет, только если ечть в меню
    i = 0
    cnt = 0
    while i < len(keyboards.menu):
        if text == keyboards.menu[i]:
            cnt += 1
        i += 1
    if cnt == 1:
        SQLighter.insert_order(id_order, SQLighter.get_alco_item_id(text), cid)
        bot.send_message(cid, "Сколько?", reply_markup=keyboards.quantity)
        userStep[cid] = consts.select_quantity_step
    else:
        bot.send_message(cid, "Выбирай из предложенных вариантов, братан")

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == consts.select_quantity_step)
def select_cnt(m):
    cid = m.chat.id
    text = m.text
    print('confirm')
    bot.send_chat_action(cid, 'typing')
    if text == "1" or text == "2" or text == "3" or text == "4" or text == "5" or text == "6" or text == "7" or text == "8" or text == "9":
        SQLighter.update_quantity_order(text,cid)
        bot.send_message(cid, "Подтверждаешь?", reply_markup=keyboards.verify)
        userStep[cid] = consts.confirm_buy
    else:
        bot.send_message(cid, "Просто выбери вариант")


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == consts.confirm_buy)
def confirm(m):
    cid = m.chat.id
    text = m.text
    print('conf')
    bot.send_chat_action(cid, 'typing')
    if text == "Да":
        SQLighter.confirm_order(1,cid)
        bot.send_message(cid, "Красава, ещё?;) /buy "
                              "Если ты все - закрывай заказ /closeOrder", reply_markup=keyboards.commands)
        # формируем итоговый заказ
        i = 0
        pos = ''
        while i < len(list(SQLighter.get_order_pos(cid))):
            item = str(SQLighter.get_order_pos(cid)[i]).replace('(\'', '').replace('\',)', '')  # удаляем скобки
            pos = pos + ', ' + item
            i = i + 1
        print(SQLighter.get_order_pos(cid))
        bot.send_message(cid, "Твой заказ " + pos[2:pos.__len__()])
        userStep[cid] = consts.null_step
    elif text == "Нет":
        SQLighter.confirm_order(0, cid)
        bot.send_message(cid, "Пидора ответ. Что-то другое? /buy "
                              "Если ты все - закрывай заказ /closeOrder", reply_markup=keyboards.commands)
        userStep[cid] = consts.null_step
    else:
        bot.send_message(cid, "Просто выбери вариант")




@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "Я тя не понял, " + str(m.chat.first_name)+ "\nПопробуй /help", reply_markup=keyboards.command)


bot.polling()
