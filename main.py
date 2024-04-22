from background import keep_alive
import random as r
import os
import telebot
import time
import requests
from googletrans import Translator

from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot(os.getenv("TOKEN"))

bot_id = bot.get_me().id



def updateLogs():
  global logs
  log_file = open('logs.txt', 'r', encoding = 'utf-8')
  logs = log_file.read().split(' ')
  log_file.close()
  global messages
  messages_file = open('messages.txt', 'r', encoding = 'utf-8')
  messages = messages_file.read().split('±gay👷‍♀️')
  messages_file.close()
  global modes
  modes_file = open('modes.txt', 'r', encoding = 'utf-8')
  modes = modes_file.read()
  modes_file.close()
updateLogs()

def Trans():
  translator = Translator()
  num = r.randint(3, 6)
  text = ""
  #for i in message.text.split():
    #text += i
    #text += " "
  #while text[-1] in " !?.":
    #text = text[:-1]
  #while ". " in text:
    #hui = text.find(". ")
    #text = text[:hui:]+text[hui+1::]
  #text += ". "
  for _ in range(num):
    text += logs[r.randint(0, len(logs)-1)] + " "
  print(text)
  result = translator.translate(text, src='ru', dest='en').text
  print(result)
  result = translator.translate(result, src='en', dest='zh-cn').text
  print(result)
  result = translator.translate(result, src='zh-cn', dest='ru').text
  print(result)
  return result#.split(".")#[-1]

def GetMessage():
  return messages[r.randint(0, len(messages)-1)]

def basedMessage():
  num = r.randint(3, 6)
  text = ""
  for _ in range(num):
    text += logs[r.randint(0, len(logs)-1)] + " "
  return text

def GetMode(id):
  for line in modes.split("\n"):
    if str(id) in line.split(":")[0]:
      print("GetMode returned ", line.split(":")[1])
      return line.split(":")[1]
  print("GetMode returned 'trans'")
  return 'trans'



@bot.message_handler(commands=["start_cringe"])
def log_start(message):
  while True:
    try:
      if GetMode(message.from_user.id)=='messages':
        bot.reply_to(message, GetMessage())
      else:
        bot.reply_to(message, Trans())
    except:
      print("fail")
    else:
      bot.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAEnVF9lQq8eq3wNB7FGOk1QlC4NRzH6rQAC_SQAAqRHsUgY4Wqfbkfb4jME', message_thread_id=message.message_thread_id, reply_to_message_id=message.id)
      break


@bot.inline_handler(lambda query: len(query.query) >= 0)
def default_query(inline_query):
  try:
    r1 = types.InlineQueryResultArticle('1', 'Задоньте', types.InputTextMessageContent('дайте денег на 4377720008037566'))
    r2 = types.InlineQueryResultArticle('2', 'Кринжануть', types.InputTextMessageContent("@bibbucrat_logbot"))
    bot.answer_inline_query(inline_query.id, [r1, r2])
  except Exception as e:
    print(e)



@bot.message_handler(commands=["donate"])
def Donate(message):
  bot.reply_to(message, "Дима, задонь на 4377720008037566")

@bot.message_handler(commands=["switch"])
def switch(message):
  global modes
  mods=['trans', 'messages']
  id=0
  for line in modes.split("\n"):
    if str(message.from_user.id) in line.split(":")[0]:
      writer = open('modes.txt', 'w', encoding = 'utf-8')
      id=str(line.split(":")[0])
      if line.split(":")[1]==mods[0]:
        modes = modes.replace(line, id+":"+mods[1])
        bot.reply_to(message, "Вы в режиме сообщений")
      else:
        modes = modes.replace(line, id+":"+mods[0])
        bot.reply_to(message, "Вы в режиме перевода")
      writer.write(modes)
      writer.close()
      updateLogs()
      break
      
  if id==0:
    idlogs = open('modes.txt', 'w', encoding = 'utf-8')
    modes += "\n"+str(message.from_user.id)+":"+mods[0]
    idlogs.write(modes)
    bot.reply_to(message, "Вы в режиме слов")
    idlogs.close()
    updateLogs()
    



@bot.message_handler(commands=["r", "говно"])
def shit(message):
  if message.reply_to_message != None:
    if message.reply_to_message.from_user.id == bot_id:
      updateLogs()
      try:
        messages_file = open('messages.txt', 'r', encoding = 'utf-8')
        text = messages_file.read()
        messages_new = open('messages.txt', 'w', encoding = 'utf-8')
        text = text.replace(message.reply_to_message.text+"±gay👷‍♀️", "")
        messages_new.write(text)
        messages_file.close()
        messages_new.close()
        updateLogs()
        print("success")
        while True:
          try:
            if GetMode(message.from_user.id)=='messages':
              bot.reply_to(message, GetMessage())
            else:
              bot.reply_to(message, Trans())
          except:
            print("fail")
          else:
            break
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.reply_to_message.message_id)
      except:
        print("no such element")


@bot.message_handler(commands=["viser_antona"])
def viser(message):
  pass




@bot.message_handler(func=lambda msg: True)
def logging(message):
  text = message.text.split(" ")
  log_write = open('logs.txt', 'a', encoding = 'utf-8')
  for w in text:
    if len(w) >0 and w[0] == "/":
      continue
    nuzhnoe_slovo = ""
    for s in w:
      if s.isalpha() or s == "-":
        nuzhnoe_slovo += s.lower()
    if nuzhnoe_slovo not in logs and "http" not in nuzhnoe_slovo and nuzhnoe_slovo[0] != "@":
      log_write.write(nuzhnoe_slovo)
      log_write.write(" ")
  messages_write = open('messages.txt', 'a', encoding = 'utf-8')
  if message.text not in messages and "http" not in message.text and "@" not in message.text and "бот" not in message.text.lower() and 'цитат' not in message.text.lower() and message.text[0] != "/" and  '##'  not in message.text:
    messages_write.write(message.text)
    messages_write.write("±gay👷‍♀️")
  updateLogs()
  log_write.close()
  messages_write.close()
  if (message.reply_to_message != None and message.reply_to_message.from_user.id == bot_id) or r.randint(0, 80) == 0:
    while True:
      try:
        if GetMode(message.from_user.id)=='messages':
          bot.reply_to(message, GetMessage())
        else:
          bot.reply_to(message, Trans())
      except:
        print("fail")
      else:
        break
  elif "бот, дай опрос" in message.text.lower():
    while True:
      try:
        bot.send_poll(message.chat.id, Trans(),[Trans(),Trans(),Trans()], is_anonymous=False, allows_multiple_answers=True, message_thread_id=message.message_thread_id, reply_to_message_id=message.id)
      except:
        print("fail poll")
      else:
        break

@bot.message_handler(content_types=['photo', 'audio', 'video', 'document', 'location', 'contact', 'sticker', 'animation'])
def media_handler(message):
      if message.reply_to_message != None:
        if message.reply_to_message.from_user.id == bot_id or r.randint(0, 80) == 0:
          while True:
            try:
              if GetMode(message.from_user.id)=='messages':
                bot.reply_to(message, GetMessage())
              else:
                bot.reply_to(message, Trans())
            except:
              print("fail")
            else:
              break



keep_alive()
while True:
  bot.polling(non_stop = True)