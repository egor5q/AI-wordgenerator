# -*- coding: utf-8 -*-
import os
import telebot
import time
import random
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient


token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)


client=MongoClient(os.environ['database'])
db=client.aiwordgen
words=db.words


try:
    pass

except Exception as e:
    print('Ошибка:\n', traceback.format_exc())
    bot.send_message(441399484, traceback.format_exc())

    
@bot.message_handler()
def addword(m):
    if m.from_user.id!=m.chat.id:
        toupdate={}
        allword=words.find_one({})
        textwords=m.text.split(' ')
        i=0
        for ids in textwords:
            currentword=ids
            if currentword=='&start':
                currentword='start'
            if i==0:
                toupdate.update({'&start':{ids:1}})
            end=False
            try:
                nextword=textwords[i+1]
            except:
                nextword='&end'
                end=True
            if nextword=='&end' and end==False:
                nextword='end'
            if ids not in toupdate:     
                toupdate.update({currentword:{nextword:1}})
            else:
                if nextword not in toupdate[currentword]:
                    toupdate[currentword].update({nextword:1})
                else:
                    toupdate[currentword][nextword]+=1
            i+=1
            
        for ids in toupdate:
            if ids not in allword['words']:
                words.update_one({},{'$set':{'words.'+str(ids):toupdate[ids]}})
            else:
                for idss in toupdate[ids]:
                    if idss not in allword['words'][ids]:
                        words.update_one({},{'$set':{'words.'+str(ids)+'.'+str(idss):allword[ids][idss]}})
                    else:
                        words.update_one({},{'$inc':{'words.'+str(ids)+'.'+str(idss):allword[ids][idss]}})
                        
        toprint=words.find_one({})
        print(toprint)
                                       
            
        
    
    
print('7777')
bot.polling(none_stop=True,timeout=600)

