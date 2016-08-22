# -*- coding: utf-8 -*-

import telebot, time, urllib, urllib2, json

from telebot import types # Tipos para la API del bot.
from transantiago import getParada, getLocationParada

try:
    from local_settings import *
except ImportError, e:
    pass

bot = telebot.TeleBot(TOKEN)

def listener(messages):

    for m in messages:
        cid = m.chat.id

        if m.content_type == 'text':
            print "[" + str(cid) + "]: " + m.text

        elif m.content_type == 'location':
            bot.send_message(cid, 'Ubicación recibida con éxito. Estoy obteniendo los paraderos cercanos')

            latitude    = m.location.latitude
            longitude   = m.location.longitude

            getLocationParada(bot, cid, latitude, longitude)

        else:
            print m.content_type

bot.set_update_listener(listener)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Hola')

#Parada
@bot.message_handler(commands=['parada'])
def command_parada(m):
    cid = m.chat.id
    bot.send_message(cid, 'Estoy buscando la información del paradero...')

    parada = m.text[len('/parada '):]
    parada = parada.upper()

    getParada(bot, cid, parada)


bot.polling(none_stop=True)
