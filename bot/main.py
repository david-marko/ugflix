from config import bot, state, check_bot, check_subscriptions, check_user, create_keyboard, get_state, commands, red, host
from functions import db, dbhost, dbname
import requests
from telebot import types
#from payment import *
#from movies import *

used_commands = [
    'Mobile Money',
    "Movies",
    "English Movies",
    "Translated Movies",
    "Renew",
    "Get Access",
    "Visa or MasterCard",
    "Crypto",
    "Home"
]

@bot.message_handler(commands=['start', 'Back_home', 'start_over'])
def start_command(message):
    state[message.chat.id] = 'start'
    if not check_user(message):
        user_id = message.from_user.id
        f_name = message.from_user.first_name
        username = message.from_user.username
        last_id = db("INSERT INTO `users` (`id`, `user_id`, `first_name`, `username`, `Created`, `Comment`, `Status`) VALUES (NULL, '" +
                     str(user_id)+"', '"+f_name+"', '"+username+"', current_timestamp(), '', '1');", 'insert')
        # Add free trial
        db("INSERT INTO `subscription`(`id`, `user_id`, `Plan`, `Created`, `Next_billing`) VALUES (NULL," +
           str(user_id)+",'Free',CURRENT_TIMESTAMP(),date_add(CURRENT_TIMESTAMP(),interval 5 day));", 'insert')
    if check_bot(message):
        bot.reply_to(message, "We are sorry, this account is not allowed")
    else:
        check_sub = check_subscriptions(message)
        if check_sub[0] == True:
            if check_sub[2] == 'Free':
                bot.reply_to(message, "Your %s trial plan has been activated for %s days" % (
                    check_sub[2], str(check_sub[1])))
            else:
                bot.reply_to(message, "Your %s plan is active and expires in %s days" % (
                    check_sub[2], str(check_sub[1])))
            state[message.chat.id] = 'home'
            bot.reply_to(message, "Welcome to your one source of entertainment for Translated and Non-translated Movies / Series", 
                         reply_markup=create_keyboard(['Search', 'Latest', 'Continue', 'Movies', 'Series', '/Help']))
        else:
            state[message.chat.id] = 'renew'
            bot.reply_to(message, "Renew Your Subscription", reply_markup=create_keyboard(['Get Access', 'Back']))

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = str(message.from_user.id)
    f_name = message.from_user.first_name
    username = message.from_user.username
    query = message.text
    last_page = red.get(user_id).decode()
    print(query, last_page)
    if last_page == 'Search' and message.text != 'Back':
        # Perform search here and return results
        pass
    elif last_page == 'English Movies' or last_page == 'Translated Movies':
        if query is not 'Back':
            category = message.text
            sql = "SELECT (`Title`+' '+`Year`) as 'Movie' FROM `movies` WHERE `is_translated` = 1 AND `Category` = '"+category+"' ORDER BY `Year`,`id` DESC LIMIT 0,50"
            movies = db(sql,'many')
            keyboard = types.InlineKeyboardMarkup()
            titles = []
            for each in movies:
                keyboard.add(types.InlineKeyboardButton(each['Movie']))
                titles.append(each['Movie'])
            bot.send_message(message.chat.id, "Here is a list of 50 Latest English Movies under "+category)
            bot.send_message(message.chat.id, "Use Search button on /start to quickly find a movie")
            bot.send_message(message.chat.id, category+" English Movies", 
                            reply_markup=keyboard)
            bot.reply_to(message, "Choose what you want to watch", reply_markup=create_keyboard(['Back']))
    # Check if state is search and parse the text sent
    # Check if state is english or translated movies, show list from categories
    if query in used_commands:
        red.set(user_id, query)
        if query == "Home":
            bot.reply_to(message, "Welcome to your one source of entertainment for Translated and Non-translated Movies / Series", 
                         reply_markup=create_keyboard(['Search', 'Latest', 'Continue', 'Movies', 'Series', '/Help']))
        elif query == 'Renew':
            bot.reply_to(message, "Get Monthly Access", reply_markup=create_keyboard(['Get Access', 'Back']))
        elif query == 'Get Access':
            bot.reply_to(message, "Make Payment of 12,000 UGX or 5 USD to get access for one month", 
                     reply_markup=create_keyboard(['Mobile Money','Visa or  MasterCard','Crypto','Back']))
        elif query == 'Mobile Money' or query == 'Visa or MasterCard' or query == 'Crypto':
            if query == 'Mobile Money':
                url = host+"/payment/momo"
            elif query == "Visa or MasterCard":
                url = host+"/payment/card"
            elif query == "Crypto":
                url = host+"/payment/cyrpto"
            r = requests.get(url, params={
                "user_id": user_id,
                "first_name": f_name,
                "username": username
            })
            if r.status_code == 200:
                link = r.json()['link']
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(
                    text="Make Secure Payment",
                    web_app=types.WebAppInfo(url=link)
                ))
                bot.send_message(message.chat.id, "Select /start when done with payment", reply_markup=keyboard)
                bot.send_message(
                    message.chat.id, "🔒 Make Payment with your preferred currency")
                # bot.send_message(message.chat.id, link)
            else:
                bot.send_message(
                    message.chat.id, "There was an error. Please contact admin @admin")
        elif query == 'Home':
            bot.reply_to(message, "Welcome to your one source of entertainment for Translated and Non-translated Movies / Series", 
                         reply_markup=create_keyboard(['Search', 'Latest', 'Continue', 'Movies', 'Series', '/Help']))
        elif query == 'Search':
            bot.reply_to(message, "Search for a movie or series by Name or Title", 
                         reply_markup=create_keyboard(['Back']))
        elif query == 'Movies':
            bot.reply_to(message, "Choose what you want to watch", reply_markup=create_keyboard(['Translated Movies', 'English Series', 'Back']))
        elif query == 'Translated Movies':
            categories = db("SELECT DISTINCT `Category` FROM `movies` WHERE `is_translated` = 1 GROUP BY `Category` ASC ORDER BY movies.Category ASC;", 'many')
            cats = []
            for each in categories:
                cats.append(each['Category'])
            cats.append('Back')
            bot.reply_to(message, "Find you favorite Translated Movies from the Categories Below", 
                        reply_markup=create_keyboard(cats))
        elif query == 'English Movies':
            categories = db("SELECT DISTINCT `Category` FROM `movies` WHERE `is_translated` = 0 GROUP BY `Category` ASC ORDER BY movies.Category ASC;", 'many')
            cats = []
            for each in categories:
                cats.append(each['Category'])
            cats.append('Back')
            bot.reply_to(message, "Find you favorite English Movies from the Categories Below", 
                        reply_markup=create_keyboard(cats))
        elif query == 'Series':
            pass
        elif query == 'Translated Series':
            pass
        elif query == 'English Series':
            pass
        elif query == 'Continue Watching':
            pass
    elif message.text == 'Back':
        # last_page = red.get(user_id)
        if last_page == 'Search':
            bot.reply_to(message, "Welcome to your one source of entertainment for Translated and Non-translated Movies / Series", 
                         reply_markup=create_keyboard(['Search', 'Latest', 'Continue', 'Movies', 'Series', '/Help']))
        if last_page == 'Movies':
            red.set(user_id, 'Home')
            bot.reply_to(message, "Welcome to your one source of entertainment for Translated and Non-translated Movies / Series", 
                         reply_markup=create_keyboard(['Search', 'Latest', 'Continue', 'Movies', 'Series', '/Help']))
        elif last_page == 'English Movies' or last_page == 'Translated Movies':
            red.set(user_id, 'Movies')
            bot.reply_to(message, "Choose what you want to watch", reply_markup=create_keyboard(['Translated Movies', 'English Series', 'Back']))
    else:
        bot.reply_to(message, "We could not identify that command. /start")

# @bot.message_handler(func=lambda message: get_state(message.chat.id) == 'home')
# def option1_command(message):
#     if message.text == 'Search':
#         state[message.chat.id] = 'search'
#         bot.reply_to(message, "Find Movie or Series by replying with the name or title", reply_markup=create_keyboard(['Back']))
#     elif message.text == 'Continue':
#         state[message.chat.id] = 'Continue'
#         bot.reply_to(message, "Continue Watching Series from you last episode", reply_markup=create_keyboard(['Back']))
#     elif message.text == 'Latest':
#         state[message.chat.id] = 'latest'
#         bot.reply_to(message, "Latest Releases", reply_markup=create_keyboard(['Back']))
#     elif message.text == 'Movies':
#         state[message.chat.id] = 'movies'
#         bot.reply_to(message, commands['start'], reply_markup=create_keyboard(['Translated Movies', 'English Series']))
#     elif message.text == 'Series':
#         state[message.chat.id] = 'series'
#         bot.reply_to(message, commands['start'], reply_markup=create_keyboard(['Translated Series', 'English Series']))

@bot.message_handler(commands=["Help"])  # user command
def start(m, res=False):
    state[m.chat.id] = 'start'
    bot.send_message(m.chat.id, "Help: For any help, please contact @admin")

bot.infinity_polling()