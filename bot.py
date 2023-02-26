import telebot
from telebot import types
from functions import *
import requests

bot = telebot.TeleBot(bot_token)
bot_name = "UGFlix"
host = "https://ugflix.vercel.app"

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    if not check_user(message):
        user_id = message.from_user.id
        f_name = message.from_user.first_name
        username = message.from_user.username
        last_id = db("INSERT INTO `users` (`id`, `user_id`, `first_name`, `username`, `Created`, `Comment`, `Status`) VALUES (NULL, '"+str(user_id)+"', '"+f_name+"', '"+username+"', current_timestamp(), '', '1');", 'insert')
        # Add free trial
        db("INSERT INTO `subscription`(`id`, `user_id`, `Plan`, `Created`, `Next_billing`) VALUES (NULL,"+str(user_id)+",'Free',CURRENT_TIMESTAMP(),date_add(CURRENT_TIMESTAMP(),interval 5 day));", 'insert')
    # if bot, dont allow
    if check_bot(message):
        bot.reply_to(message, "We are sorry, this account is not allowed")
    else:
        # Check subscription
        check_sub = check_subscriptions(message)
        if check_sub[0] == True:
            bot.reply_to(message, "Hello %s, Welcome to %s " % (message.from_user.first_name, bot_name))
            if check_sub[2] == 'Free':
                bot.reply_to(message, "Your %s trial plan has been activated for %s days" % (check_sub[2], str(check_sub[1])))
            else:
                bot.reply_to(message, "Your %s plan is active and expires in %s days" % (check_sub[2], str(check_sub[1])))
            markup = types.ReplyKeyboardMarkup(row_width=2)
            itembtn1 = types.KeyboardButton('Popular')
            itembtn2 = types.KeyboardButton('Series')
            itembtn3 = types.KeyboardButton('Movies')
            itembtn4 = types.KeyboardButton('Help')
            markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
            bot.send_message(message.chat.id, "Select Category of Translated and Non-Translated Movies", reply_markup=markup)
        else:
            keyboard = types.ReplyKeyboardMarkup(row_width=1)
            # Create a custom keyboard button
            button = types.KeyboardButton('/renew')
            # Add the button to the keyboard layout
            keyboard.add(button)
            bot.reply_to(message, "Hello %s, Your %s Plan expired %s days ago" % (message.from_user.first_name, check_sub[2], str(check_sub[1])), reply_markup=keyboard)
    
@bot.message_handler(commands=['renew'])
def renew_options(message, res=False):
    print("Renewing")
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Mobile Money (12,000 ugx)')
    itembtn2 = types.KeyboardButton('Card (5 USD)')
    itembtn4 = types.KeyboardButton('Crypto (5 USD)')
    markup.add(itembtn1, itembtn2, itembtn4)
    bot.send_message(message.chat.id, "Choose Option to pay $5 Monthly Premium access:", reply_markup=markup)
    # bot.send_message(message.chat.id, "Choose Option to pay $5 Monthly Premium access:")

@bot.message_handler(commands=['Mobile Money (12,000 ugx)'])
def momo_renew(message, res=False):
    user_id = message.from_user.id
    f_name = message.from_user.first_name
    username = message.from_user.username
    r = requests.get(host+"/payment/momo", params={
        "user_id": user_id,
        "first_name": f_name,
        "username": username
    })
    if r.status_code == 200:
        link = r.json()['link']
        bot.send_message(message.chat.id, "Click the link below to securely complete the payment of 12,000 ugx using mobile money (MTN or Airtel)")
        bot.send_message(message.chat.id, link)
    else:
        bot.send_message(message.chat.id, "There was an error. Admin has been contacted")




@bot.message_handler(commands=["help"]) # user command
def start(m, res=False):
    bot.send_message(m.chat.id, "Help: ")

@bot.message_handler(commands=['forward'], content_types=['text','video','photo'])
def forward_video(message):
    # Forward a video from your channel to the user
    video_id = '3'
    # bot.for
    # bot.kick_chat_member(chat_id='@meandiug', user_id=1609763046)
    bot.forward_message(chat_id=message.chat.id, from_chat_id='@meandiug', message_id=video_id)

bot.infinity_polling()