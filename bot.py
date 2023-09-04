import telebot
from telebot import types


TOKEN = '5869718003:AAEzj09510rQ62GRsrFpWAB4tMbdlcL2BLk'
YOUR_CHANNEL_ID = '-1001959485469'
PASSWORD = '1234'  # Здесь указывается ваш пароль
DATABASE_FILE = 'database.txt'  # Путь к файлу базы данных

bot = telebot.TeleBot(TOKEN)


# Флаг, указывающий, прошла ли верификация пользователя
verified_users = {}


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton('Обращение жильцов')
    item2 = telebot.types.KeyboardButton('Передача показаний')
    item3 = telebot.types.KeyboardButton('О компании')
    item4 = telebot.types.KeyboardButton('Связаться с диспетчером')

    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id,
                     'Привет, {0.first_name}.\n\n🤖Я электронный диспетчер управляющей компании.\n\nС моей помощью Вы можете:\n\n📌узнать об отключении воды и ремонтных работах в Вашем доме.\n\n📌 подсказать управляющему, что именно волнует жильцов Вашего дома.\n\n📌сможете отправить показания счетчиков, просто сделав их фото.\n\nТеперь в один клик (!) можно получать новости из разных каналов (!!) в одной папке 🤩\n\nСобрали для вас 3 полезных группы нашего района, ссылка на папку с группами ⬇️\nhttps://t.me/addlist/Zm7faHv80180ZTYy \n\nВведите пароль⬇️'.format(
                         message.from_user), reply_markup=markup, disable_web_page_preview=True)


@bot.message_handler(commands=['user'])
def add_user_to_database(message):
    user_id = message.chat.id  # Получить user_id из объекта message
    if is_user_in_database(user_id):
        bot.send_message(user_id, "Вы уже есть в базе данных")
    else:
        with open(DATABASE_FILE, 'a') as file:
            file.write(str(user_id) + '\n')
        bot.send_message(user_id, "Вы были добавлены в базу данных")


def is_user_in_database(user_id):
    with open(DATABASE_FILE, 'r') as file:
        for line in file:
            if str(user_id) == line.strip():
                return True
    return False

@bot.message_handler(commands=['echo'])
def handle_echo_command(message):
    if len(message.text.split()) > 1:
        # Получаем текст сообщения после команды /echo
        echo_message = ' '.join(message.text.split()[1:])
        send_echo_message(echo_message)
        bot.reply_to(message, "Сообщение отправлено всем пользователям.")
    else:
        bot.reply_to(message, "Вы не указали текст сообщения.")


@bot.message_handler(commands=['sendgif'])
def send_gif(message):
    chat_id = message.chat.id
    gif_path = '/home/SpasiboTaras/image1.gif'  # путь к вашему GIF-файлу

    with open(gif_path, 'rb') as gif:
        bot.send_document(chat_id, gif)

def optimize_gif(input_gif):
    output_gif = 'optimized.gif'  # Выходное имя файла после оптимизации
    return output_gif

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    message_text = message.text
    chat_id = message.chat.id

    if chat_id not in verified_users:
        # Пользователь не прошел верификацию, запрашиваем пароль
        if message_text == PASSWORD:
            # Пользователь ввел правильный пароль, прошла верификация
            verified_users[chat_id] = True
            bot.send_message(chat_id, 'Вы успешно прошли верификацию!\n\nМожете продолжать использование бота.')
        else:
            # Пользователь ввел неправильный пароль
            bot.send_message(chat_id, 'Неправильный пароль. Попробуйте снова.')

    # Пользователь прошел верификацию, обрабатываем сообщения
    else:
        if message_text == 'Передача показаний':
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            item5 = telebot.types.KeyboardButton('Текст')
            item6 = telebot.types.KeyboardButton('Фото')
            back = telebot.types.KeyboardButton('⬅️Назад')

            markup.add(item5, item6, back)

            bot.send_message(chat_id,
                             '📮Для передачи показаний счетчиков Вы можете воспользоваться двумя способами:\n\n📝Текст. Вам будет предложено по порядку передать показания счетчика холодной, а затем горячей воды. Вы вносите показания просто набирая цифры.\n\n📷Фото. В этом режиме всё ещё проще. Вы отправляете фото счётчиков.\n\nКнопка /start вернет вас в главное меню',
                             reply_markup=markup)

        elif message_text == "Обращение жильцов":
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            item7 = telebot.types.KeyboardButton('Сообщение')
            back = telebot.types.KeyboardButton('⬅️Назад')

            markup.add(item7, back)

            bot.send_message(chat_id,
                             '📝Вы можете написать нам о любой проблеме в Вашем доме.\n\n📌Течёт батарея\n📌Плохо убран подъезд\n📌Не работает домофон\n📌Нахамил наш работник\n\nИ многое другое, о чем сочтете нужным уведомить нас. Кроме этого мы будем рады получать отзывыо нашей работе и Ваши пожелания.\n\nКнопка /start вернет вас в главное меню',
                             reply_markup=markup)
            bot.register_next_step_handler(message, process_tenant_message)

        elif message_text == "О компании":
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = telebot.types.KeyboardButton('⬅️Назад')
            item10 = telebot.types.KeyboardButton('/user')
            markup.add(back, item10)

            bot.send_message(chat_id,
                             'Компания "Управляющая Компания" основана в 2005 году. Основное направление деятельности – управление и обслуживание многоквартирных домов. В настоящее время обслуживается 35 домов в городе.\n- Адрес: ул. Пушкина, д.14, офис 88\n\nКонтактные данные:\nРуководитель - Иванов Иван Иванович.\n📞Телефон: +7 (123) 111-22-33\n📬Email: company@mail.ru\n\nЭлектрик - Артёмов Геннадий Викторович.\n📞Телефон: +7 (684) 331-83-23\n\nСлесарь - Петров Иван Сергеевич.\n📞Телефон: +7 (124) 611-23-33\n\nКнопка /start вернет вас в главное меню',
                             reply_markup=markup)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton('⬅️Назад')

            markup.add(back)
        elif message_text == "/user":
            add_user_to_database(message)

        elif message_text == "Связаться с диспетчером":
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            item8 = telebot.types.KeyboardButton('Сообщение')
            back = telebot.types.KeyboardButton('⬅️Назад')

            markup.add(item8, back)

            bot.send_message(chat_id,
                             '📞Связаться с диспетчером\nВы можете по телефону\n+7 (123) 456-78-90 \n\n⚡️Или оставить сообщение и диспетчер сам свяжется с Вам.\n\nКнопка /start вернет вас в главное меню',
                             reply_markup=markup)
            bot.register_next_step_handler(message, process_contact_message)

        elif message_text == "⬅️Назад":
            if message.chat.type == 'private':
                markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = telebot.types.KeyboardButton('Обращение жильцов')
                item2 = telebot.types.KeyboardButton('Передача показаний')
                item3 = telebot.types.KeyboardButton('О компании')
                item4 = telebot.types.KeyboardButton('Связаться с диспетчером')

                markup.add(item1, item2, item3, item4)

                bot.send_message(chat_id, 'Главное меню', reply_markup=markup)
            else:
                bot.send_message(message.chat.id, 'Главное меню',
                                 reply_markup=types.ReplyKeyboardRemove())
        elif message_text == "Текст":
            bot.send_message(chat_id, 'Введите номер квартиры')
            bot.register_next_step_handler(message, process_apartment_number)
        elif message_text == "Фото":
            bot.send_message(chat_id, 'Введите номер квартиры')
            bot.register_next_step_handler(message, process_apartment_number2)


def process_apartment_number(message):
    apartment = message.text
    bot.send_message(message.chat.id, 'Введите фамилию собственника')
    bot.register_next_step_handler(message, process_owner_surname, apartment)


def process_apartment_number2(message):
    apartment2 = message.text
    bot.send_message(message.chat.id, 'Введите фамилию собственника')
    bot.register_next_step_handler(message, process_owner_surname2, apartment2)


def process_owner_surname(message, apartment):
    owner_surname = message.text
    bot.send_message(message.chat.id, 'Введите показания счетчика холодной воды')
    bot.register_next_step_handler(message, process_cold_water, apartment, owner_surname)


def process_owner_surname2(message, apartment2):
    owner_surname2 = message.text
    bot.send_message(message.chat.id, 'Введите показания счетчика холодной воды')
    bot.register_next_step_handler(message, process_counter_photo2, apartment2, owner_surname2)


def process_cold_water(message, apartment, owner_surname):
    cold_water = message.text
    bot.send_message(message.chat.id, 'Введите показания счетчика горячей воды')
    bot.register_next_step_handler(message, process_hot_water, apartment, owner_surname, cold_water)


def process_hot_water(message, apartment, owner_surname, cold_water):
    hot_water = message.text

    message_to_send5 = f'💧💧💧Показания воды\n\nНомер квартиры: {apartment}\nФамилия собственника: {owner_surname}\nПоказания счетчика холодной воды: {cold_water}\nПоказания счетчика горячей воды: {hot_water}'

    bot.send_message(message.chat.id,
                     '🤝Спасибо за передачу показаний!\n\nКнопка /start вернет вас в главное меню',
                     reply_markup=telebot.types.ReplyKeyboardRemove())

    # Отправляем сообщение диспетчеру в закрытый канал
    bot.send_message(YOUR_CHANNEL_ID, message_to_send5)


def process_tenant_message(message):
    if message.text == 'Сообщение':
        bot.send_message(message.chat.id, 'Введите ваше сообщение')
        bot.register_next_step_handler(message, send_tenant_message)
    elif message.text == '⬅️Назад':
        # Вернуться в главное меню
        start(message)


def send_tenant_message(message):
    tenant_message = message.text

    message_to_send2 = f'🗒Обращение жильцов\n\n{tenant_message}'

    bot.send_message(message.chat.id,
                     '🤝Спасибо за обращение!\n\nКнопка /start вернет вас в главное меню',
                     reply_markup=telebot.types.ReplyKeyboardRemove())

    # Отправляем сообщение диспетчеру в закрытый канал
    bot.send_message(YOUR_CHANNEL_ID, message_to_send2)


def process_contact_message(message):
    if message.text == 'Сообщение':
        bot.send_message(message.chat.id, 'Введите ваше сообщение')
        bot.register_next_step_handler(message, send_contact_message)
    elif message.text == '⬅️Назад':
        # Вернуться в главное меню
        start(message)


def send_contact_message(message):
    contact_message = message.text

    message_to_send3 = f'⚡️⚡️⚡️Срочно диспетчеру\n\n{contact_message}'

    bot.send_message(message.chat.id,
                     '🤝Спасибо за обращение!\n\nКнопка /start вернет вас в главное меню',
                     reply_markup=telebot.types.ReplyKeyboardRemove())

    # Отправляем сообщение диспетчеру в закрытый канал
    bot.send_message(YOUR_CHANNEL_ID, message_to_send3)


def process_counter_photo2(message, apartment2, owner_surname2):
    if message.content_type == 'photo':
        # Получите идентификатор фотографии
        photo_id = message.photo[-1].file_id

        # Сгенерируйте сообщение с подписью фотографии
        message_to_send4 = f'💧💧📷Показания с фотографией\n\nНомер квартиры: {apartment2}\nФамилия собственника: {owner_surname2}'

        # Отправьте фотографию и сообщение в закрытый канал
        bot.send_photo(YOUR_CHANNEL_ID, photo_id, caption=message_to_send4)

        bot.send_message(message.chat.id,
                         '🤝Спасибо за передачу показаний с фотографией!\n\nКнопка /start вернет вас в главное меню',
                         reply_markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True))
    else:
        bot.send_message(message.chat.id,
                         'Придется начать все заново. Вы не прикрепили фотографию счетчика./start .')

def send_echo_message(message):
    users = load_users()
    for user_id in users:
        try:
            bot.send_message(user_id, message)
        except Exception as e:
            print(f"Ошибка при отправке сообщения пользователю {user_id}: {str(e)}")

def load_users():
    with open(DATABASE_FILE, 'r') as file:
        users = [line.strip() for line in file]
    return users
bot.polling()
