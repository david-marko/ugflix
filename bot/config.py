import telebot
from telebot import types
from functions import *
import requests
import re
import redis

bot = telebot.TeleBot(bot_token)
bot_name = "UGFlix"
host = "https://ugflix.vercel.app"

redis_host = "redis-18179.c244.us-east-1-2.ec2.cloud.redislabs.com"
port = 18179
password = "GqRUKfxeoNBuPmwIIRxuoKWgQRHWr9eG"
red = redis.Redis(host=redis_host, port=port, db=0, password=password)

admin = "someboddy"
bot = telebot.TeleBot('6162698092:AAHCqdH2_3HBhBaF_cfC-t_GA_KP5QmwSDw')

# Define the initial state
state = {}

# Define the commands that the user can use
commands = {
    'start': 'Welcome to my bot! Please choose an option:', # Check Subscription
    'renew': 'You chose option 1. What would you like to do next?', 
    'home': 'You chose option 2. What would you like to do next?',
    'search': 'You chose option 2. What would you like to do next?',
    'continue': 'You chose option 2. What would you like to do next?',
    'series': 'You chose option 2. What would you like to do next?',
    'movies': 'You chose option 2. What would you like to do next?',
    'help': 'For support, please contact @admin',
    'back': 'Going back to the previous menu.'
}

# Define the helper functions
def create_keyboard(options):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [telebot.types.KeyboardButton(option) for option in options]
    keyboard.add(*buttons)
    return keyboard

def get_state(chat_id):
    return state.get(chat_id, 'start')