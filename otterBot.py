#! /usr/bin/python3.7
import logging
import telegram
from time import sleep
from telegram.error import NetworkError, Unauthorized
from io import BytesIO
from PIL import Image
from functools import wraps
from restrict import restricted
import configparser

config = configparser.ConfigParser()
config.read('config.txt')
botToken = config['DEFAULT']['botToken']
update_id = None

#function prototypes
def otter(bot,update):
    _otter(bot,update)
def mau(bot,update):
    _mau(bot,update)
def schleck(bot,update):
    _schleck(bot,update)

#functions to be called + triggerwords
fl =    [[otter,["Get-Image", "Whiteboard"]],
        [mau,["mau","Mau"]],
        [schleck,["schleck","Schleck","mlem","Mlem","vlem","Vlem"]]]

#custom keyboard keys
key =   [['Get-Image'],['Schleck']]

#custom functions
@restricted
def _otter(bot,update):
    #Todo Webcam
    pass

@restricted
def _schleck(bot,update):
    image = Image.open('schleck.jpg')
    bio = BytesIO()
    bio.name = 'image.jpeg'
    image.save(bio, 'JPEG')
    bio.seek(0)
    bot.send_photo(update.message.chat_id, photo=bio)

@restricted
def _mau(bot,update):
    bot.send_message(update.message.chat_id, text="mau")


###########
@restricted
def keyboard(bot,update):
    reply_markup = telegram.ReplyKeyboardMarkup(key)
    bot.send_message(chat_id=update.message.chat_id,text="Chirp!",reply_markup=reply_markup)


def echo(bot):
    global update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        if update.message:
            for f in fl:
                if(update.message.text in f[1]):
                    keyboard(bot,update)
                    f[0](bot,update)

def main():
    bot = telegram.Bot(token=botToken)

    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            update_id += 1

if __name__ == '__main__':
    main()
