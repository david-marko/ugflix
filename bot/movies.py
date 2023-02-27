from config import bot, get_state, create_keyboard, state
from functions import db, dbname
from telebot import types

@bot.message_handler(func=lambda message: get_state(message.chat.id) == 'movies')
def renew_handler(message):
    if message.text == 'Translated Movies':
        state[message.chat.id] = 'translated_movies'
        # Fetch categories from database
        categories = db("SELECT DISTINCT `Category` FROM `movies` WHERE `is_translated` = 1 GROUP BY `Category` ASC ORDER BY movies.Category ASC;", 'many')
        cats = []
        for each in categories:
            cats.append(each['Category'])
        cats.append('Back')
        bot.reply_to(message, "Find you favorite Translated Movies", 
                     reply_markup=create_keyboard(cats))
    elif message.text == 'English Movies':
        state[message.chat.id] = 'english_movies'
        categories = db("SELECT DISTINCT `Category` FROM `movies` WHERE `is_translated` = 0 GROUP BY `Category` ASC ORDER BY movies.Category ASC;", 'many')
        cats = []
        for each in categories:
            cats.append(each['Category'])
        cats.append('Back')
        bot.reply_to(message, "Find you favorite Translated Movies", 
                     reply_markup=create_keyboard(cats))
    elif message.text == 'Back':
        state[message.chat.id] = 'movies'
        bot.reply_to(message, "Choose what you want to watch", reply_markup=create_keyboard(['Translated Movies', 'English Series', '/Back_home']))

@bot.message_handler(func=lambda message: get_state(message.chat.id) == 'translated_movies')
def translated(message):
    category = message.text
    if category == 'Back':
        state[message.chat.id] = 'movies'
        bot.reply_to(message, "Choose what you want to watch", reply_markup=create_keyboard(['Translated Movies', 'English Series', '/Back_home']))
    else:
        sql = "SELECT (`Title`+' '+`Year`) as 'Movie' FROM `movies` WHERE `is_translated` = 1 AND `Category` = 'Action' ORDER BY `Year`,`id` DESC LIMIT 0,50"
        movies = db(sql,'many')
        print(movies)
        keyboard = types.InlineKeyboardMarkup()
        titles = []
        for each in movies:
            keyboard.add(types.InlineKeyboardButton(each['Movie']))
            titles.append(each['Movie'])
        bot.send_message(message.chat.id, "Here is a list of 50 Latest Translated Movies under "+category)
        bot.send_message(message.chat.id, "Use Search button on /start to quickly find a movie")
        bot.send_message(message.chat.id, category+" Translated Movies", 
                        reply_markup=keyboard)
        bot.reply_to(message, "Choose what you want to watch", reply_markup=create_keyboard(['Back']))
    
    # Gets a list from database. Pagination required

@bot.message_handler(func=lambda message: get_state(message.chat.id) == 'english_movies')
def translated(message):
    category = message.text
    if category == 'Back':
        state[message.chat.id] = 'movies'
        categories = db("SELECT DISTINCT `Category` FROM `movies` WHERE `is_translated` = 0 GROUP BY `Category` ASC ORDER BY movies.Category ASC;", 'many')
        cats = []
        for each in categories:
            cats.append(each['Category'])
        cats.append('Back')
        bot.reply_to(message, "Find you favorite Movies", 
                     reply_markup=create_keyboard(cats))
    else:
        sql = "SELECT (`Title`+' '+`Year`) as 'Movie' FROM `movies` WHERE `is_translated` = 0 AND `Category` = '"+category+"' ORDER BY `Year`,`id` DESC LIMIT 0,50"
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


@bot.message_handler(func=lambda message: get_state(message.chat.id) == 'details')
def details(message):
    if message.text == 'watch':
        pass
    else:
        pass

@bot.message_handler(func=lambda message: get_state(message.chat.id) == 'watch')
def details(message):
    pass