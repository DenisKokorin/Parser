import telebot
from telebot import types
import requests
from telebot.types import ReplyKeyboardRemove

bot = telebot.TeleBot("7144814670:AAHXsWdZoxGosVprJbEjIiJGXai5W2QH4-0")

@bot.message_handler(commands=['start'])
def greeting(message):
    bot.send_message(message.chat.id, "Напишите ваш запрос", reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, choice_num)

def choice_num(message):
    global request
    request = message.text
    msg = bot.send_message(message.chat.id, "Сколько вакансий вам нужно?")
    bot.register_next_step_handler(msg, find_vacancy)

def find_vacancy(message):
    global num
    num = message.text
    if num.isdigit() == False:
        bot.send_message(message.chat.id, "Введите только число")
        bot.register_next_step_handler(message, find_vacancy)
    else:
        bot.send_message(message.chat.id, "Запрос обрабатывается...")
        r = requests.get(url=f"http://app:80/{request}", params={"num": num})
        bot.send_message(message.chat.id, r.json())
        if r.json() == "К сожалению парсер не смог найти никаких вакансий. Попробуйте сделать другой запрос":
            bot.register_next_step_handler(message, greeting)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton("Не имеет значения")
            markup.add(btn)
            bot.send_message(message.chat.id, "Напишите город", reply_markup=markup)
            bot.register_next_step_handler(message, choice_city)

def choice_city(message):
    global city
    city = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("не требуется")
    btn2 = types.KeyboardButton("1–3 года")
    btn3 = types.KeyboardButton("3–6 лет")
    btn4 = types.KeyboardButton("более 6 лет")
    btn5 = types.KeyboardButton("Не имеет значения")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id,"Выберите опыт работы", reply_markup=markup)
    bot.register_next_step_handler(message, choice_experience)

def choice_experience(message):
    global experience
    experience = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Полная занятость")
    btn2 = types.KeyboardButton("Частичная занятость")
    btn3 = types.KeyboardButton("Стажировка")
    btn4 = types.KeyboardButton("Проектная работа/разовое задание")
    btn5 = types.KeyboardButton("Волонтерство")
    btn6 = types.KeyboardButton("Не имеет значения")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id, "Выберите тип занятости", reply_markup=markup)
    bot.register_next_step_handler(message, choice_type_of_employment)

def choice_type_of_employment(message):
    global type_of_employment
    type_of_employment = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("полный день")
    btn2 = types.KeyboardButton("удаленная работа")
    btn3 = types.KeyboardButton("гибкий график")
    btn4 = types.KeyboardButton("сменный график")
    btn5 = types.KeyboardButton("Вахтовый метод")
    btn6 = types.KeyboardButton("Не имеет значения")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id, "Выберите график работы", reply_markup=markup)
    bot.register_next_step_handler(message, choice_schedule)

def choice_schedule(message):
    schedule = message.text
    r = requests.get(url=f"http://app:80/{request}/filtered", params={"req": request, "num": num, "city": city, "experience": experience, "type_of_employment": type_of_employment, "schedule": schedule})
    for vacancy in r.json():
        answer = f'Вакансия: {vacancy['title']}, зарплата: {vacancy['salary']}, работодатель: {vacancy['company']}, требуемый опыт работы: {vacancy['experience']}, тип занятости: {vacancy['type_of_employment']}, график работы: {vacancy['schedule']}, сейачс эту вакансию смотрят: {vacancy['viewers_count']}, ссылка: {vacancy['link']}'
        bot.send_message(message.chat.id, answer, reply_markup=ReplyKeyboardRemove())
    bot.send_message(message.chat.id,"Вы можете просмотреть все вакансии, которые есть в базе с помощью команды /all или сделать  новый запрос", reply_markup=ReplyKeyboardRemove())

@bot.message_handler(commands=['all'])
def show_all_vacancy(message):
    r = requests.get(url="http://app:80/all")
    for vacancy in r.json():
        answer = f'Вакансия: {vacancy['title']}, зарплата: {vacancy['salary']}, работодатель: {vacancy['company']}, требуемый опыт работы: {vacancy['experience']}, тип занятости: {vacancy['type_of_employment']}, график работы: {vacancy['schedule']}, сейачс эту вакансию смотрят: {vacancy['viewers_count']}, ссылка: {vacancy['link']}'
        bot.send_message(message.chat.id, answer, reply_markup=ReplyKeyboardRemove())

bot.infinity_polling()

