import telebot
from keyboards import *
import module as m

bot = telebot.TeleBot('1753135807:AAHny8IXYQwV2kZo5R2kdB4dX2Ozfpgylzg')
test_dict = {}

keyboard_menu = get_keyboard_menu()
course_menu = get_course_menu()
test_list = get_test_list()
keyboard_cont = get_keyboard_cont()
keyboard_cont_check = get_keyboard_check()

start_menu = "Добро пожаловать в стартовое меню! Для вас доступны следующие варианты: \n" + \
             "1. Список курсов " + "\n2. Продолжить изучение курса" + \
             "\n3. Тесты по пройденному материалу" "\n4. Статистика"

course_message = "Меню курсов. Для вас доступны следующие варианты: \n" + \
             "1. Курс №1: " + '"' + str(m.get_message("1.0.0")) + '"' \
             + "\n2. Курс №2: " + '"' + str(m.get_message("2.0.0"))

test_message = "Выберете тест из предложенных:" + "\n1.Основы Python (лёгкий)"


@bot.message_handler(commands=['start'])
def start_message(message):
    m.add_user(int(message.chat.id))
    m.set_level(int(message.chat.id), "1.0.0")
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


def test_menu(message):
    print("test menu")
    msg = bot.send_message(message.chat.id, start_menu, reply_markup=keyboard_menu)
    bot.register_next_step_handler(msg, course_start)


def course_start(message):
    print("cource_start")
    try:
        num = int(message.text)
        if num > 4:
            bot.send_message(message.chat.id, "Я тебя не понял.")
            menu_message(message)
        if num == 1:
            msg = bot.send_message(message.chat.id, course_message, reply_markup=course_menu)
            bot.register_next_step_handler(msg, chouse_course)
        elif num == 2:
            course_continue(message)
        elif num == 3:
            chouse_test(message)
        elif num == 4:
            statistics(message)

    except ValueError:
        bot.send_message(message.chat.id, "Я тебя не понял.")
        menu_message(message)


def chouse_course(message):
    if message.text == "Меню":
        menu_message(message)
        return 
    try:
        num = int(message.text)
        m.set_level(message.chat.id, str(num) + ".1.0")
        course_continue(message)
    except ValueError:
        bot.send_message(message.chat.id, "Я тебя не понял.")
        menu_message(message)


def course_continue(message):
    print("cource_cont")
    if message.text == "Меню":
        menu_message(message)
    elif message.text == "1" or message.text == "2" or message.text == "3" or message.text == "Продолжить":
        if m.get_next(m.get_user_level(message.chat.id)) is None:
            bot.send_message(message.chat.id,
                             "Что-ж, вот вы и закончили этот курс! Посмотрите, что еще мы можем вам предложить: ")
            m.pass_course(message.chat.id, m.get_user_level(message.chat.id))
            m.set_level(message.chat.id, "1.0.0")
            menu_message(message)
        else:
            if m.get_answer(m.get_user_level(str(message.chat.id))) is None:
                if m.has_image(m.get_user_level(message.chat.id)):
                    image = m.get_image(m.get_user_level(message.chat.id))
                    bot.send_photo(message.chat.id, image)
                bot.send_message(message.chat.id,
                                 m.get_message(m.get_user_level(message.chat.id)), reply_markup=keyboard_cont)
                m.set_level(message.chat.id, m.get_next(m.get_user_level(message.chat.id))[0])
                bot.register_next_step_handler(message, course_continue)
            else:
                if m.has_image(m.get_user_level(message.chat.id)):
                    image = m.get_image(m.get_user_level(message.chat.id))
                    bot.send_photo(message.chat.id, image)
                bot.send_message(message.chat.id,
                                 m.get_message(m.get_user_level(message.chat.id)), reply_markup=keyboard_cont_check)
                bot.register_next_step_handler(message, check_answer)

    elif message.text == "/help":
        help_message(message)
    else:
        bot.send_message(message.chat.id, "Я тебя не понял.")
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
            m.set_level(message.chat.id, m.get_next(m.get_user_level(message.chat.id))[0])
            bot.register_next_step_handler(msg, course_continue)
            return
        else:
            m.set_level(message.chat.id, m.get_next(m.get_user_level(message.chat.id))[1])
            msg = bot.send_message(message.chat.id, m.get_message(m.get_user_level(message.chat.id)),
                                   reply_markup=keyboard_cont_check)
            bot.register_next_step_handler(msg, check_answer)


def chouse_test(message):
    print("choce test")
    msg = bot.send_message(message.chat.id, test_message,
                           reply_markup=test_list)
    bot.register_next_step_handler(msg, test_start)


def test_start(message):
    print("test 1 started")
    if message.text == "Меню":
        menu_message(message)
        return
    if message.text == "1":
        test_dict[message.chat.id] = 0
        test1_keys = get_test1()
        bot.send_message(message.chat.id, "Тест по основам Python\n"
                                          "1. Какая функция выводит что-либо в консоль?",
                         reply_markup=test1_keys)


def test_result(message):
    print("result")
    res = test_dict[message.chat.id]
    if res == 4:
        bot.send_message(message.chat.id, "Ваш балл за тест: 4/4\n"
                                          "Вы превосходно освоили основы языка. Теперь можете изучать его на "
                                          "углубленном уровне")
    elif 1 < res < 4:
        bot.send_message(message.chat.id, f"Ваш балл за тест: {res}/4\n"
                                          f"Вам лучше повторить основы синтаксиса чтобы перейти к более сложному "
                                          f"материалу")
    else:
        bot.send_message(message.chat.id, f"Ваш балл за тест: {res}/4\n"
                                          f"Советуем вам перепройти курс по основам Python, знания языка оставляют "
                                          f"желать лучшего")

    m.pass_test1(message.chat.id, test_dict[message.chat.id])
    test_menu(message)


def statistics(message):
    stat = m.statistics(message.chat.id)
    if stat[0] == 'pass':
        stat[0] = "Пройден ✅"
    else:
        stat[0] = "Не пройден ❌"
    if stat[1] == 'pass':
        stat[1] = "Пройден ✅"
    else:
        stat[1] = "Не пройден ❌"
    if stat[2] is None:
        stat[2] = "Не пройден ❌"
    else:
        stat[2] = str(stat[2]) + "/4"
    ans = "Ваша статистика по курам и тестам:" + "\n1. Курс №1: " + stat[0] + "\n2. Курс №2: " + stat[1] + \
          "\n3. Тест №1: " + stat[2]
    bot.send_message(message.chat.id, ans)
    menu_message(message)


@bot.callback_query_handler(func=lambda call: call.data.split('.')[0] == '1')
def callback_test1(call):
    bot.answer_callback_query(callback_query_id=call.id)
    if call.data.split('.')[1] == '4':
        test_dict[call.message.chat.id] += 1
    test2_keys = get_test2()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='2.Где правильно заданная переменная? (вариант ответа, который не выдаст ошибку '
                               'при запуске\n',
                          reply_markup=test2_keys)


@bot.callback_query_handler(func=lambda call: call.data.split('.')[0] == '2')
def callback_test2(call):
    bot.answer_callback_query(callback_query_id=call.id)
    if call.data.split('.')[1] == '3':
        test_dict[call.message.chat.id] += 1
    test3_keys = get_test3()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Что покажет код?\n'
                               'for i in range(5):\n '
                               '   if i % 2 == 0:\n'
                               '      continue\n'
                               '   print(i)\n',
                          reply_markup=test3_keys)


@bot.callback_query_handler(func=lambda call: call.data.split('.')[0] == '3')
def callback_test3(call):
    bot.answer_callback_query(callback_query_id=call.id)
    if call.data.split('.')[1] == '1':
        test_dict[call.message.chat.id] += 1
    test4_keys = get_test4()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Что покажет код?\n"
                                   "for j in 'Hi! I\'m mister Robert':\n"
                                   "   if j == '\'':\n"
                                   "      print('Найдено')\n"
                                   "      break\n"
                                   "   else:\n"
                                   "      print ('Готово')\n",
                              reply_markup=test4_keys)


@bot.callback_query_handler(func=lambda call: call.data.split('.')[0] == '4')
def callback_test4(call):
    bot.answer_callback_query(callback_query_id=call.id)
    if call.data.split('.')[1] == '1':
        test_dict[call.message.chat.id] += 1
    bot.answer_callback_query(callback_query_id=call.id)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"Поздравляем с прохождением теста! Ознакомьтесь с результатами, выберете "
                               f"следующий тест или продолжите обучение")
    test_result(call.message)



bot.polling()
