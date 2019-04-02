# -*- coding: utf-8 -*-
import os
import telebot
import time
import random
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient
from nltk.tokenize import sent_tokenize, word_tokenize


token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)


client=MongoClient(os.environ['database'])
db=client.
users=db.users


try:
    pass

except Exception as e:
    print('Ошибка:\n', traceback.format_exc())
    bot.send_message(441399484, traceback.format_exc())

    
@bot.message_handler()
def addword(m):
    textwords=word_tokenize(i)
    x=words.find_one({'word':})
    for ids in x:
        
    
    
print('7777')
bot.polling(none_stop=True,timeout=600)

