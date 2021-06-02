import telebot
import module as m

bot = telebot.TeleBot('1753135807:AAHny8IXYQwV2kZo5R2kdB4dX2Ozfpgylzg')

keyboard_menu = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard_menu.row("1", "2", "3")

keyboard_cont = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard_cont.row("Продолжить", "Меню")

keyboard_cont_check = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard_cont_check.row("Меню")

start_menu = "Добро пожаловать в стартовое меню! Для вас доступны следующие варианты: \n1." + \
             str(m.get_message("1.0.0")) \
             + "\n2." + str("2.0.0") + "\n3. Продолжить"


@bot.message_handler(commands=['start'])
def start_message(message):
    m.add_user(int(message.chat.id))
    m.set_level(int(message.chat.id), "1.1.0")
    print(message.chat)
    bot.send_message(message.chat.id, "Добро пожаловать в нашего обучающего бота!")
    menu_message(message)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Моли о помощи.....')
    menu_message(message)


def menu_message(message):
    print("menu_message")
    msg = bot.send_message(message.chat.id, start_menu, reply_markup=keyboard_menu)
    bot.register_next_step_handler(msg, course_start)


def course_start(message):
    print("cource_start")
    try:
        num = int(message.text)
        if num > 3:
            bot.send_message(message.chat.id, "Я тебя не понял1.")
            menu_message(message)
        if num == 1 or num == 2:
            m.set_level(message.chat.id, str(num) + ".1.0")
            course_continue(message)
        elif num == 3:
            course_continue(message)

    except ValueError:
        bot.send_message(message.chat.id, "Я тебя не понял2.")
        menu_message(message)


def course_continue(message):
    print("cource_cont")
    if message.text == "Меню":
        menu_message(message)
    elif message.text == "1" or message.text == "2" or message.text == "3" or message.text == "Продолжить":
        if m.get_next(m.get_user_level(message.chat.id)) is None:
            bot.send_message(message.chat.id,
                             "Что-ж, вот вы и закончили этот курс! Посмотрите, что еще мы можем вам предложить: ")
            m.set_level(message.chat.id, "1.0.0")
            menu_message(message)
        else:
            if m.get_answer(m.get_user_level(str(message.chat.id))) is None:
                bot.send_message(message.chat.id,
                                 m.get_message(m.get_user_level(message.chat.id)), reply_markup=keyboard_cont)
                if m.has_image(m.get_user_level(message.chat.id)):
                    image = m.get_image(m.get_user_level(message.chat.id))
                    bot.send_photo(message.chat.id, image)
                m.set_level(message.chat.id, m.get_next(m.get_user_level(message.chat.id))[0])
                bot.register_next_step_handler(message, course_continue)
            else:
                bot.send_message(message.chat.id,
                                 m.get_message(m.get_user_level(message.chat.id)), reply_markup=keyboard_cont_check)
                bot.register_next_step_handler(message, check_answer)

    else:
        bot.send_message(message.chat.id, "Я тебя не понял2.")
        menu_message(message)


def check_answer(message):
    print("check_answer")
    if message.text == "Меню":
        menu_message(message)
    else:
        ans = m.get_answer(m.get_user_level(str(message.chat.id)))
        if message.text == ans:
            m.set_level(message.chat.id, m.get_next(m.get_user_level(message.chat.id))[0])
            msg = bot.send_message(message.chat.id, m.get_message(m.get_user_level(message.chat.id)),
                                   reply_markup=keyboard_cont)
            bot.register_next_step_handler(msg, course_continue)
            return
        else:
            m.set_level(message.chat.id, m.get_next(m.get_user_level(message.chat.id))[1])
            msg = bot.send_message(message.chat.id, m.get_message(m.get_user_level(message.chat.id)),
                                   reply_markup=keyboard_cont)
            bot.register_next_step_handler(msg, check_answer)


bot.polling()
