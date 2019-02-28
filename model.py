import sqlite3

import config

path = config.path + "triggerBot.db"



def addTrigger(message):
    trigger = message.text.replace("/add_trigger ", "").lower()

    dataBase = sqlite3.connect( path )
    cursorDataBase = dataBase.cursor()

    cursorDataBase.execute("SELECT text FROM triggers WHERE trigger = '%s' AND chatId = '%s'" % (trigger, message.chat.id))
    row = cursorDataBase.fetchone()
    if row is None:
        update = False
    else:
        update = True

    if message.reply_to_message.text is not None:
        triggerText = str(message.reply_to_message.text)
        triggerType = 'text'
    elif message.reply_to_message.sticker is not None:
        triggerText = str(message.reply_to_message.sticker.file_id)
        triggerType = 'sticker'
    elif message.reply_to_message.photo is not None:
        triggerText = str(message.reply_to_message.photo[0].file_id)
        triggerType = 'photo'
    elif message.reply_to_message.video is not None:
        triggerText = str(message.reply_to_message.video.file_id)
        triggerType = 'video'
    elif message.reply_to_message.voice is not None:
        triggerText = str(message.reply_to_message.voice.file_id)
        triggerType = 'voice'
    elif message.reply_to_message.document is not None:
        triggerText = str(message.reply_to_message.document.file_id)
        triggerText = 'document'
    elif message.reply_to_message.audio is not None:
        triggerText = str(message.reply_to_message.audio.file_id)
        triggerType = 'audio'
    elif message.reply_to_message.video_note is not None:
        triggerText = str(message.reply_to_message.video_note.file_id)
        triggerType = 'video_note'

    if update:
        cursorDataBase.execute("UPDATE triggers SET type = '%s', text = '%s' WHERE chatId = %s AND trigger = '%s'" % (triggerType, triggerText, int(message.chat.id), trigger))
        dataBase.commit()
    else:
        cursorDataBase.execute("INSERT INTO triggers (chatId, trigger, type, text) VALUES (%s, '%s', '%s', '%s')" % (int(message.chat.id), trigger, triggerType, triggerText))
        dataBase.commit()

    cursorDataBase.close()
    dataBase.close()





def delTrigger(message):
    trigger = message.text.replace("/del_trigger ", "").lower()

    dataBase = sqlite3.connect( path )
    cursorDataBase = dataBase.cursor()

    cursorDataBase.execute("DELETE FROM triggers WHERE chatId = %s AND trigger = '%s'" % (message.chat.id, trigger))
    dataBase.commit()

    cursorDataBase.close()
    dataBase.close()





def listTriggers(message):
    dataBase = sqlite3.connect( path )
    cursorDataBase = dataBase.cursor()

    cursorDataBase.execute("SELECT trigger FROM triggers WHERE chatId = %s" % (message.chat.id))
    row = cursorDataBase.fetchone()
    index = 0
    list = ''
    while row is not None:
        index += 1
        list += str(index) + ") " + row[0] + "\n"
        row = cursorDataBase.fetchone()

    if list:
        return list
    else:
        return "no triggers in this chat\n\n/add_trigger {trigger}"






def findTrigger(message):
    dataBase = sqlite3.connect( path  )
    cursorDataBase = dataBase.cursor()

    cursorDataBase.execute("SELECT type, text FROM triggers WHERE chatId = %s AND trigger = '%s'" % (message.chat.id, message.text.lower() ) )
    row = cursorDataBase.fetchone()

    if row is not None:
        return row
    else:
        return None
