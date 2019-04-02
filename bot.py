# -*- coding: utf-8 -*-
import os
import telebot
import time
import random
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient
import traceback


token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)


client=MongoClient(os.environ['database'])
db=client.aiwordgen
words=db.words

endsymbols=['!', '.', '?']

try:
    pass

except Exception as e:
    print('Ошибка:\n', traceback.format_exc())
    bot.send_message(441399484, traceback.format_exc())

 
@bot.message_handler(commands=['story'])
def story(m):
    if m.from_user.id==441399484 or m.from_user.id==197216910:
        try:
            sentences=random.randint(1,3)
            try:
                sentences=int(m.text.split(' ')[1])
            except:
                pass
            csent=0
            ctext=''
            allwords=words.find_one({})
            while csent<sentences:
                cword=0
                currentword=None
                while currentword!='&end':
                    start=None
                    if cword==0:
                        start=allwords['words']['&start']
                        items=[]
                        for ids in start:
                            i=0
                            while i<start[ids]: 
                                items.append(ids)
                                i+=1
                        start=random.choice(items)
                        i=0
                        cwd=''
                        currentword=start
                        st=0
                        for a in start:
                            if i==0 and a.isupper()==False and st==0:
                                if a!='@':
                                    cwd+=a.upper()
                            else:
                                if a!='@':
                                    cwd+=a
                            st+=1
                        start=cwd
                        ctext+=start+' '
                    else:
                        nextwords=[]
                        for ids in allwords['words'][currentword]:
                            i=0
                            while i<allwords['words'][currentword][ids]:
                                nextwords.append(ids)
                                i+=1
                        nextword=random.choice(nextwords)
                        if currentword[len(currentword)-1] in endsymbols:
                            endsent=1
                        else:
                            endsent=0
                        currentword=nextword
                        if nextword!='&end':
                            i=0
                            cwd=''
                            for a in nextword:
                                if a!='@':
                                    cwd+=a
                            ctext+=cwd+' '
                        else:
                            if endsent==0:
                                ctext=ctext[:len(ctext)-1]
                                ctext+='.'
                        
                    cword+=1
                csent+=1
                ctext+=' '
            bot.send_message(m.chat.id, ctext)
        except Exception as e:
            bot.send_message(441399484, traceback.format_exc())
            


@bot.message_handler()
def addword(m):
    if m.from_user.id!=m.chat.id:
        try:
            if m.text[0]!='/':
                toupdate={}
                allword=words.find_one({})
                textwords=m.text.split(' ')
                i=0
                for ids in textwords:
                  if ids not in endsymbols:
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
                        try:
                            if currentword[len(currentword)-1] == '.':
                                currentword=currentword[:len(currentword)-1]
                        except:
                            pass
                    if nextword=='&end' and end==False:
                        nextword='end'
                    try:
                        if currentword[len(currentword)-1] in endsymbols:
                            nextword='&end'
                            if currentword[len(currentword)-1] == '.':
                                currentword=currentword[:len(currentword)-1]
                    except:
                        pass
                    if currentword not in toupdate:     
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
                                words.update_one({},{'$set':{'words.'+str(ids)+'.'+str(idss):toupdate[ids][idss]}})
                            else:
                                words.update_one({},{'$inc':{'words.'+str(ids)+'.'+str(idss):toupdate[ids][idss]}})
        except Exception as e:
            bot.send_message(441399484, traceback.format_exc())
            
        
    
    
print('7777')
bot.polling(none_stop=True,timeout=600)

