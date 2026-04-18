import telebot
from telebot import types

# Замените "ТОКЕН_ВАШЕГО_БОТА" на ваш реальный токен
BOT_TOKEN = "8527355722:AAHQlxA8k9aH3T0UfVH2ehTRKgPTrErijlY"
bot = telebot.TeleBot(BOT_TOKEN)

# Словарь для хранения меню для каждого пользователя
user_menus = {}

# Словарь для хранения подменю "меню"
main_menu_options = {
    "магазин": "Переход в магазин.",
    "профиль": "Просмотр вашего профиля.",
    "арена": "Вход на арену.",
    "крафт": "Мастерская крафта.",
    "задания": "Список доступных заданий."
}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_get_card = types.KeyboardButton("получить карту")
    btn_menu = types.KeyboardButton("меню")
    btn_my_cards = types.KeyboardButton("мои карты")
    btn_clan = types.KeyboardButton("клан")

    # Располагаем кнопки в два ряда
    markup.row(btn_get_card, btn_menu)
    markup.row(btn_my_cards, btn_clan)

    bot.send_message(message.chat.id, "Добро пожаловать! Выберите действие:", reply_markup=markup)

# Обработчик кнопок основной клавиатуры
@bot.message_handler(func=lambda message: message.text in ["получить карту", "меню", "мои карты", "клан"])
def handle_main_buttons(message):
    chat_id = message.chat.id
    text = message.text

    if text == "получить карту":
        bot.send_message(chat_id, "Вы получили новую карту!")
        # Здесь будет логика получения карты

    elif text == "меню":
        # Создаем клавиатуру для подменю "меню"
        menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for option in main_menu_options.keys():
            menu_markup.add(types.KeyboardButton(option))
        menu_markup.add(types.KeyboardButton("назад")) # Кнопка для возврата в главное меню

        user_menus[chat_id] = "main_menu" # Отмечаем, что пользователь в подменю "меню"
        bot.send_message(chat_id, "Выберите раздел меню:", reply_markup=menu_markup)

    elif text == "мои карты":
        bot.send_message(chat_id, "Вот список ваших карт.")
        # Здесь будет отображение карт пользователя

    elif text == "клан":
        bot.send_message(chat_id, "Информация о клане.")
        # Здесь будет информация о клане

# Обработчик кнопок подменю "меню" и команды "назад"
@bot.message_handler(func=lambda message: message.chat.id in user_menus)
def handle_submenu(message):
    chat_id = message.chat.id
    text = message.text

    if user_menus.get(chat_id) == "main_menu":
        if text == "назад":
            # Возвращаемся в главное меню
            user_menus.pop(chat_id, None) # Удаляем запись о подменю
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_get_card = types.KeyboardButton("получить карту")
            btn_menu = types.KeyboardButton("меню")
            btn_my_cards = types.KeyboardButton("мои карты")
            btn_clan = types.KeyboardButton("клан")
            markup.row(btn_get_card, btn_menu)
            markup.row(btn_my_cards, btn_clan)
            bot.send_message(chat_id, "Возвращаемся в главное меню. Выберите действие:", reply_markup=markup)
        elif text in main_menu_options:
            bot.send_message(chat_id, main_menu_options[text])
            # Здесь может быть дальнейшая логика для каждого пункта меню
        else:
            bot.send_message(chat_id, "Пожалуйста, выберите пункт из меню или нажмите 'назад'.")
    else:
        # Если пользователь вдруг оказался в этом обработчике, но не в подменю,
        # отправляем его в главное меню
        send_welcome(message)


# Запуск бота
if name == 'main':
    bot.polling(none_stop=True)