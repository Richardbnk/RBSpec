
"""
# Developer: Richard Raphael Banak
# Objective: Functions to help ETL from files and other tools for python automation
# Creation date: 2022-05-26
"""

import telegram
import os
import urllib
import json

BOT_API_TOKEN = "5540996635:AAF7bH-csckqsLZHsYf3PCzsBOSRvkVOn8g"
RHCENTER_CHAT_ID = "-776091231"

# NEW BOT: Include bot on any group, the look for any updates on:
#    https://api.telegram.org/bot<YourBOTToken>/getUpdates


def send(
    message,
    chat_id,
):
    global BOT_API_TOKEN

    bot = telegram.Bot(token=BOT_API_TOKEN)
    bot.sendMessage(chat_id=chat_id, text=message)
