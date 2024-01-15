
""" Бот доступен по ссылке @euphoriaseshopsbot"""



import telebot
from telebot import types
import requests

TOKEN = '6906935919:AAGPEk4qmdmPCHwA9IxlNGmLMKxdtSnnehg'
bot = telebot.TeleBot(TOKEN)

def make_sorting_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add('До 150', 'Больше 150')
    keyboard.add('Унисекс', 'Мужское', 'Женское')
    keyboard.add('Все товары', 'БОНУС')
    return keyboard
@bot.message_handler(func=lambda message: message.text == "БОНУС")
def handle_bonus(message):
    bot.send_message(message.chat.id, "Группа ChocoPy31 лучше всех!\nУдачи всем командам!")
    
    bot.send_photo(message.chat.id, 'https://ibb.co/m9681DD')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Выберите категорию товаров:', reply_markup=make_sorting_keyboard())

@bot.message_handler(func=lambda message: message.text in ['До 150', 'Больше 150', 'Унисекс', 'Мужское', 'Женское', 'Все товары'])
def handle_message(message):
    try:
        response = requests.get('http://euphoriastore.hopto.org/api/fragnance/')  
        if response.status_code == 200:
            products_data = response.json()
            filtered_products = []

            for product in products_data['results']:
                if message.text == "До 150" and float(product['price']) <= 150:
                    filtered_products.append(product)
                elif message.text == "Больше 150" and float(product['price']) > 150:
                    filtered_products.append(product)
                elif message.text == "Унисекс" and "унисекс" in product['description'].lower():
                    filtered_products.append(product)
                elif message.text == "Мужское" and "мужчин" in product['description'].lower():
                    filtered_products.append(product)
                elif message.text == "Женское" and "унисекс" not in product['description'].lower() and "мужчин" not in product['description'].lower():
                    filtered_products.append(product)
                elif message.text == "Все товары":
                    filtered_products.append(product)

            for product in filtered_products:
                send_product_info(message, product)
        else:
            bot.send_message(message.chat.id, 'Не удалось получить данные о товарах.')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e}')

def send_product_info(message, product):
    product_info = f"ID: {product['id']}\n" + \
                   f"Название: {product['title']}\n" + \
                   f"Бренд: {product['brand']}\n" + \
                   f"Цена: {product['price']}\n" + \
                   f"Размер: {product['size']}\n" + \
                   f"Доступность: {product['available']}\n" + \
                   f"Рейтинг: {product['rating']}\n" + \
                   f"Описание: {product['description']}\n"

    if 'image' in product and product['image']:
        bot.send_photo(message.chat.id, product['image'], caption=product_info)
    else:

        bot.send_message(message.chat.id, product_info)
bot.polling()