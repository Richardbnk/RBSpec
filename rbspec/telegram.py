"""
# Developer: Richard Raphael Banak
# Objective: Functions to help send messages through Telegram 
# Creation date: 2022-05-26
#
# NEW BOT: Include bot on any group, the look for any updates on:
#    https://api.telegram.org/bot<YourBOTToken>/getUpdates
"""
import telegram
from telegram import ParseMode
import os
import urllib
import json


def send(
    message,
    chat_id,
    bot_token,
):
    bot = telegram.Bot(token=bot_token)
    bot.sendMessage(chat_id=chat_id, text=message, parse_mode=ParseMode.HTML)
