
from telebot import types
import consts
from SQLighter import SQLighter
import re

class keyboards:
    #сформируем список товаров
    # Формируем клавиатуры
    menu = []
    vodkaKey = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    i = 0
    while i < len(list(SQLighter.get_alco_item(consts.vodka))):
        menu_item = str(SQLighter.get_alco_item(consts.vodka)[i]).replace('(', '').replace(',)',
                                                                                              '')  # удаляем скобки
        menu.append(menu_item[1:menu_item.__len__() - 1])
        vodkaKey.add(menu_item[1:menu_item.__len__() - 1])
        i = i + 1

    beerKey = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    i = 0
    while i < len(list(SQLighter.get_alco_item(consts.beer))):
        menu_item = str(SQLighter.get_alco_item(consts.beer)[i]).replace('(', '').replace(',)', '')  # удаляем скобки
        menu.append(menu_item[1:menu_item.__len__() - 1])
        beerKey.add(menu_item[1:menu_item.__len__() - 1])
        i = i + 1
    absentKey = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    i = 0
    while i < len(list(SQLighter.get_alco_item(consts.absent))):
        menu_item = str(SQLighter.get_alco_item(consts.absent)[i]).replace('(', '').replace(',)',
                                                                                               '')  # удаляем скобки
        menu.append(menu_item[1:menu_item.__len__() - 1])
        absentKey.add(menu_item[1:menu_item.__len__() - 1])
        i = i + 1
    vineKey = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    i = 0
    while i < len(list(SQLighter.get_alco_item(consts.vine))):
        menu_item = str(SQLighter.get_alco_item(consts.vine)[i]).replace('(', '').replace(',)', '')  # удаляем скобки
        menu.append(menu_item[1:menu_item.__len__() - 1])
        vineKey.add(menu_item[1:menu_item.__len__() - 1])
        i = i + 1
    tekillaKey = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    i = 0
    while i < len(list(SQLighter.get_alco_item(consts.tekilla))):
        menu_item = str(SQLighter.get_alco_item(consts.tekilla)[i]).replace('(', '').replace(',)',
                                                                                                '')  # удаляем скобки
        menu.append(menu_item[1:menu_item.__len__() - 1])
        tekillaKey.add(menu_item[1:menu_item.__len__() - 1])
        i = i + 1
    ginKey = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    i = 0
    while i < len(list(SQLighter.get_alco_item(consts.gin))):
        menu_item = str(SQLighter.get_alco_item(consts.gin)[i]).replace('(', '').replace(',)', '')  # удаляем скобки
        menu.append(menu_item[1:menu_item.__len__() - 1])
        ginKey.add(menu_item[1:menu_item.__len__() - 1])
        i = i + 1
    likerKey = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    i = 0
    while i < len(list(SQLighter.get_alco_item(consts.liker))):
        menu_item = str(SQLighter.get_alco_item(consts.liker)[i]).replace('(', '').replace(',)',
                                                                                              '')  # удаляем скобки
        menu.append(menu_item[1:menu_item.__len__() - 1])
        likerKey.add(menu_item[1:menu_item.__len__() - 1])
        i = i + 1
    romKey = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    i = 0
    while i < len(list(SQLighter.get_alco_item(consts.rom))):
        menu_item = str(SQLighter.get_alco_item(consts.rom)[i]).replace('(', '').replace(',)', '')  # удаляем скобки
        menu.append(menu_item[1:menu_item.__len__() - 1])
        romKey.add(menu_item[1:menu_item.__len__() - 1])
        i = i + 1
    wiskeyKey = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    i = 0
    while i < len(list(SQLighter.get_alco_item(consts.wiskey))):
        menu_item = str(SQLighter.get_alco_item(consts.wiskey)[i]).replace('(', '').replace(',)',
                                                                                               '')  # удаляем скобки
        menu.append(menu_item[1:menu_item.__len__() - 1])
        wiskeyKey.add(menu_item[1:menu_item.__len__() - 1])
        i = i + 1

    alcoSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    alcoSelect.add('Водка', 'Пиво', 'Ягерь', 'Вино', 'Ром', 'Виски', 'Джин', 'Абсент', 'Текилла')
    i = 0

    verify = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    verify.add('Да', 'Нет')

    confirm = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    confirm.add('Да', 'Нет', 'Отменить заказ')

    quantity = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    quantity.add('1', '2', '3', '4', '5', '6', '7', '8', '9')
    quantity.add()

    commands = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    commands.add('Добавить в заказ', 'Закончить заказ', 'Отменить заказ')

    command = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    command.add('Делать покупки')

    confirm_order = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    confirm_order.add('Да', 'Поменять адрес', 'Поменять телефон', 'Я только посмотреть хотел')

    hideBoard = types.ReplyKeyboardRemove()
