import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import telebot
from telebot import types

# Инициализация бота с вашим токеном
bot = telebot.TeleBot("7516439034:AAF59uroLK2LSSrcTjHeT5oWZ05stCazCJw")

# Название модели и устройство
model_name = 'test_trainer/checkpoint-18'
device = "cpu" if not torch.cuda.is_available() else "cuda"

# Загрузка токенизатора и модели
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)

# Переменная состояния для отслеживания выбранного ассистента
user_state = {}

# Обработчик стартовой команды и меню выбора ассистента
@bot.message_handler(commands=['start'])
def start(message):
    # Создание кнопок выбора ассистента
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton('Финансовый')
    btn2 = types.KeyboardButton('Тревел')
    markup.add(btn1, btn2)

    # Отправка сообщения с кнопками
    bot.send_message(message.chat.id, "Выберите ассистента:", reply_markup=markup)

# Обработчик выбора ассистента
@bot.message_handler(func=lambda message: message.text in ['Финансовый', 'Тревел'])
def choose_assistant(message):
    if message.text == 'Финансовый':
        user_state[message.chat.id] = 'financial'
        bot.send_message(message.chat.id, "Привет! Я ваш финансовый ассистент. Чем могу помочь?")
    elif message.text == 'Тревел':
        user_state[message.chat.id] = 'travel'
        bot.send_message(message.chat.id, "Тревел ассистент пока не активен.")

# Обработчик сообщений после выбора ассистента
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.chat.id in user_state:
        if user_state[message.chat.id] == 'financial':
            user_input = message.text  # Получение сообщения пользователя

            # Токенизация сообщения
            inputs = tokenizer(user_input, return_tensors="pt").to(device)

            # Генерация ответа
            outputs = model.generate(**inputs, prompt_lookup_num_tokens=9, use_cache=True, max_new_tokens=100)

            # Декодирование и отправка ответа пользователю
            response = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
            bot.reply_to(message, response)
        elif user_state[message.chat.id] == 'travel':
            bot.reply_to(message, "Тревел ассистент в разработке.")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, выберите ассистента, используя команду /start.")

# Запуск бота
bot.polling()
