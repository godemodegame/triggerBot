#!/usr/bin/python
# -*- coding: utf-8 -*-
import telebot
import logging

from model import addTrigger, delTrigger, listTriggers, findTrigger
import config       #config.py

# CRITICAL > ERROR > WARNING > INFO
logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)-3s]# %(levelname)-5s [%(asctime)s] %(message)s', level=logging.INFO)
logging.info("bot loaded")

bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types = ["text"])
def messageHandler(message):
    if message.chat.type == "supergroup" or message.chat.type == "group":

        # Add new trigger
        if message.text == "/add_trigger":
            bot.send_message(message.chat.id, "to add a trigger reply to the desired message <b>/add_trigger {trigger}</b>", parse_mode = "html")
        elif message.text.startswith("/add_trigger "):
            if message.reply_to_message:
                addTrigger(message)
                logging.info("new trigger - \"" + message.text.replace("/add_trigger ", "") + "\"")
                bot.send_message(message.chat.id, "trigger <b>\"" + message.text.replace("/add_trigger ", "") + "\"</b> has been added", parse_mode = "html")
            else:
                bot.send_message(message.chat.id, "you should <b>reply</b> to the desired message", parse_mode = "html")
                logging.info("can't add trigger(not reply)")

        # Delete trigger
        elif message.text == "/del_trigger":
            bot.send_message(message.chat.id, "to delete trigger <b>/del_trigger {trigger}</b>", parse_mode = "html")
        elif message.text.startswith("/del_trigger "):
            delTrigger(message)
            logging.info("trigger - \"" + message.text.replace("/del_trigger ", "") + "\" has been deleted")
            bot.send_message(message.chat.id, "trigger <b>\"" + message.text.replace("/del_trigger ", "") + "\"</b> has been deleted", parse_mode = "html")

        # List of triggers
        elif message.text == "/list_of_triggers":
            bot.send_message(message.chat.id, "<b>list of triggers:</b>\n\n" + str( listTriggers(message) ), parse_mode = "html")

        elif message.text == "ping":
            bot.send_message(message.chat.id, "pong")

        elif message.text == "/id":
            bot.send_message(message.chat.id, message.chat.id)

        # Searching triggers
        else:
            row = findTrigger(message)
            if row:
                logging.info(row[0] + " trigger ( " + row[1] + " ) in chat " + str(message.chat.id))
                if str(row[0]) == 'text':
                    bot.send_message(message.chat.id, str(row[1]))
                elif str(row[0]) == 'sticker':
                    bot.send_sticker(message.chat.id, str(row[1]))
                elif str(row[0]) == 'photo':
                    bot.send_photo(message.chat.id, str(row[1]))
                elif str(row[0]) == 'video':
                    bot.send_video(message.chat.id, str(row[1]))
                elif str(row[0]) == 'audio':
                    bot.send_audio(message.chat.id, str(row[1]))
                elif str(row[0]) == 'voice':
                    bot.send_voice(message.chat.id, str(row[1]))
                elif str(row[0]) == 'document':
                    bot.send_document(message.chat.id, str(row[1]))
                elif str(row[0]) == 'video_note':
                    bot.send_video_note(message.chat.id, str(row[1]))
            else:
                logging.info("@" + message.from_user.username + " in " + str(message.chat.id) + " wrote " + message.text)

    elif message.chat.type == "private":
        bot.send_message(message.chat.id, """<b>Hello!</b>

send reply to message /add_trigger {trigger} to add trigger
/del_trigger {trigger} to delete trigger
/list_of triggers

https://github.com/godemodegame/triggerBot
by @godemodegame
        """, parse_mode = "html")





if __name__ == '__main__':
     bot.polling(none_stop=True)
