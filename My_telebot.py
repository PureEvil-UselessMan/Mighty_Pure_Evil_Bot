#C:/Users/tramp/source/repos/PythonApplication1/PythonApplication1/photos
#C:/Users/Public/Documents/ImageProcessing/Users_images
from logging import exception
import telebot
import config
from telebot import types
import time
from requests import get
import cv2
import numpy as np
import os
from transliterate import translit

# Дополнительные функции
def adjust_gamma(image, gamma = 1.0):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)
def replyer(message):
    MypyBot.reply_to(message, message.text)
def send_error_to_user(message, error_type):
    MypyBot.send_message(message.chat.id, error_type, parse_mode='html')
    MypyBot.send_sticker(message.chat.id, open('Stickers/error.webp', 'rb'))

def create_save_path(message, images_type):
    user_images_dir = os.path.join(main_img_dir, translit(message.from_user.first_name, language_code='ru', reversed=True))
    src = os.path.join(user_images_dir, images_type + "_" + translit(message.from_user.first_name, language_code='ru', reversed=True) + ".jpg")
    return src

def send_img_text_sticker(message, img_path, text, sticker, reply_markup):
    if img_path is not None:
        try:
            MypyBot.send_photo(message.chat.id, photo=open(img_path, 'rb'))
        except:
            try:
                MypyBot.send_photo(message.chat.id, get(img_path).content)
            except:
                send_error_to_user(message, "Ошибка в получении пути к изображению")
    send = MypyBot.send_message(message.chat.id, text, parse_mode='html', reply_markup = reply_markup)
    MypyBot.send_sticker(message.chat.id, open('Stickers/{}.webp'.format(sticker), 'rb'))
    return send

main_img_dir = "C:/Users/Public/Documents/ImageProcessing/Users_images"
tokens = {"icecream": False, 'source': False, 'negative': False, 'gamma': False, 'gray': False, 'sepia': False, "counters": False}

MypyBot = telebot.TeleBot(config.TOKEN, parse_mode = None)

@MypyBot.message_handler(commands = ['start'])
def start_message(message):
  MypyBot.send_message(message.chat.id, 
                       "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, Всемогущее Всесущее Зло!\n или просто бот созданный обработать твое изображение".format(message.from_user, MypyBot.get_me()),
                       parse_mode='html', reply_markup = start_markup)
  # MypyBot.send_photo(message.chat.id, get("https://ih1.redbubble.net/image.990178510.9245/pp,840x830-pad,1000x1000,f8f8f8.jpg").content)
  MypyBot.send_sticker(message.chat.id, open('Stickers/hello.webp', 'rb'))

# Набор клавиатуры
start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_IceCrem = types.KeyboardButton("🍧 Хочу мороженку")
button_LetsWork = types.KeyboardButton("🎨 Мне нужно обработать изображение")
start_markup.add(button_IceCrem, button_LetsWork)

process_images_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
process_images_markup.add(button_LetsWork)

Filters = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_sourse = types.KeyboardButton("Исходник")
button_negative = types.KeyboardButton("Негатив")
button_gamma = types.KeyboardButton("Гамма Фильтр")
button_gray = types.KeyboardButton("Черно-белый")
button_counters = types.KeyboardButton("Выделить контуры")
button_tired = types.KeyboardButton("Устал, перерыв ?")
Filters.add(button_sourse, button_negative, button_gamma, button_gray, button_counters, button_tired)

baby_help_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_dark = types.KeyboardButton("0.5 Немного затемнить")
button_light = types.KeyboardButton("1.5 Немного осветлить")
button_enough = types.KeyboardButton("Перестань (reset brightnes)")
baby_help_markup.add(button_dark, button_light)
baby_enough_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
baby_enough_markup.add(button_dark, button_light, button_enough)

Remove_buttons = telebot.types.ReplyKeyboardRemove()

@MypyBot.message_handler(content_types = ['text'])
def StartWork(message):
    if message.text == '🍧 Хочу мороженку':
        if tokens['icecream'] == False:
            send = send_img_text_sticker(message,
                                "https://tortodelfeo.ru/wa-data/public/shop/products/88/27/2788/images/2648/2648.750.png",
                                "Упс, я уже все съела",
                                "hehe",
                                None)
            tokens['icecream'] = True
            MypyBot.register_next_step_handler(send, StartWork)
        else:
            send = send_img_text_sticker(message, None, "Думаешь что-то изменилось, пупсик ?", "he", None)
            MypyBot.register_next_step_handler(send, StartWork)
    elif message.text == '🎨 Мне нужно обработать изображение':
        markup_for_answer_two = types.InlineKeyboardMarkup(row_width = 2)
        button_Yes = types.InlineKeyboardButton("Да", callback_data='yes')
        button_No = types.InlineKeyboardButton("Нет", callback_data='no')
        markup_for_answer_two.add(button_Yes, button_No)
        send = send_img_text_sticker(message, None, 'Тебе точно есть 18 ?', "18", markup_for_answer_two)
        MypyBot.send_message(message.chat.id, "", reply_markup = Remove_buttons) 
        MypyBot.register_next_step_handler(send, handle_docs_photo)
        # Как удалить кнопки ?
    else:
        send_img_text_sticker(message, None, "Я не знаю что ответить 😢", "noanswer", start_markup)

def LetsGetWork(message):
    if message.text == 'Исходник':
        if tokens.get('sourse') == True:
            try:
                img_path = create_save_path(message, "source")
                send = send_img_text_sticker(message, img_path, "С такого ракурса стало только хуже XD", "haha", None)
                MypyBot.register_next_step_handler(send, LetsGetWork)
            except Exception as e:
                send_error_to_user(message, "Ой, а я не видела твоих фоточек еще, семпай...")
        else:
            send_error_to_user(message, "Ой, а я не видела твоих фоточек еще, семпай...")
    elif message.text == 'Негатив':
        if tokens.get('sourse') == True:
            if tokens.get('negative') == False:
                src_img_path = create_save_path(message, "source")
                img_path = create_save_path(message, "negative")
                img = cv2.imread(src_img_path)
                img_not = cv2.bitwise_not(img)
                cv2.imwrite(img_path, img_not)
                send = send_img_text_sticker(message, img_path, "Ммм, какая красивая фоточка", "looksgood", None)
                tokens['negative'] = True
                MypyBot.register_next_step_handler(send, LetsGetWork)
            else:
                img_path = create_save_path(message, "negative")
                send = send_img_text_sticker(message, img_path, "Я что тебе робот туда сюда ее преобразовывать?", "iamnotarobot")
                MypyBot.register_next_step_handler(send, LetsGetWork)
        else:
            send_error_to_user(message, "Ой, а я не видела твоих фоточек еще, семпай...")
    elif message.text == 'Черно-белый':
        if tokens.get('sourse') == True:
            if tokens.get('gray') == False:
                src_img_path = create_save_path(message, "source")
                img_path = create_save_path(message, "gray")
                img = cv2.imread(src_img_path)
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                cv2.imwrite(img_path, img_gray)
                MypyBot.send_photo(message.chat.id, photo=open(img_path, 'rb'))
                send = MypyBot.send_message(message.chat.id, "Ммм, какая красивая фоточка")
                MypyBot.send_sticker(message.chat.id, open('Stickers/looksgood.webp', 'rb'))
                tokens['gray'] = True
                MypyBot.register_next_step_handler(send, LetsGetWork)
            else:
                img_path = create_save_path(message, "gray")
                send = MypyBot.send_message(message.chat.id, "Я что тебе робот туда сюда ее преобразовывать?")
                MypyBot.send_photo(message.chat.id, photo=open(img_path, 'rb'))
                MypyBot.send_sticker(message.chat.id, open('Stickers/iamnotarobot.webp', 'rb'))
                MypyBot.register_next_step_handler(send, LetsGetWork)
        else:
            MypyBot.reply_to(message, "Ой, а я не видела твоих фоточек еще, семпай...")
            MypyBot.send_sticker(message.chat.id, open('Stickers/error.webp', 'rb'))
    elif message.text == 'Гамма Фильтр':
        if tokens.get('sourse') == True:
            if tokens.get('gamma') == False:
                send = send_img_text_sticker(message, None, "Тебе подсказать значение гамма, милашка?","mayi", baby_help_markup)
                MypyBot.register_next_step_handler(send, Gamma_Function)
            else:
                send = send_img_text_sticker(message, None, "Введи свое значение гамма, сладкий", "giveme", baby_enough_markup)
                MypyBot.register_next_step_handler(send, Gamma_Function)

        else:    
            send_error_to_user(message, "Ой, а я не видела твоих фоточек еще, семпай...")  
    elif message.text == "Выделить контуры":
        if tokens.get('sourse') == True:
            if tokens.get('counters') == False:
                src_img_path = create_save_path(message, "source")
                img_path = create_save_path(message, "counters")
                img = cv2.imread(src_img_path)
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                ret, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
                contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
                image_countered = img.copy()
                cv2.drawContours(image=image_countered, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                cv2.imwrite(img_path, image_countered)
                send = send_img_text_sticker(message, img_path, "Ах, как же я хорошо поработала", "wow", None)
                tokens['counters'] = True
                MypyBot.register_next_step_handler(send, LetsGetWork)
            else:
                img_path = create_save_path(message, "counters")
                send = send_img_text_sticker(message, img_path, "Ты уже выделял контуры, имей совесть! Я тут не без дела сижу ...", "tired")
                MypyBot.register_next_step_handler(send, LetsGetWork)
        else:
            send_error_to_user(message, "Ой, а я не видела твоих фоточек еще, семпай...")
    elif message.text == "Устал, перерыв ?":
            send = send_img_text_sticker(message, None, "Давай я тебя расслаблю ...", "relax", start_markup)
            MypyBot.register_next_step_handler(send, StartWork)
    else:
        send = send_img_text_sticker(message, None, "Я не знаю что ответить 😢", "noanswer", start_markup)
        MypyBot.register_next_step_handler(send, StartWork)

def Gamma_Function(message):
    flag = 0
    if message.text == '0.5 Немного затемнить':
        if tokens.get('gamma') == False:
            src_img_path = create_save_path(message, "source")
        else:
            src_img_path = create_save_path(message, "gamma")
        img_path = create_save_path(message, "gamma")
        img = cv2.imread(src_img_path)
        img_gamma = adjust_gamma(img, 0.5)
        img = cv2.imwrite(img_path, img_gamma)
        send = send_img_text_sticker(message, img_path, "Ух, как же красиво стало", "beautiful", Filters)
        tokens['gamma'] = True
        MypyBot.register_next_step_handler(send, LetsGetWork)
    elif message.text == '1.5 Немного осветлить':
        if tokens.get('gamma') == False:
            src_img_path = create_save_path(message, "source")
        else:
            src_img_path = create_save_path(message, "gamma")
        img_path = create_save_path(message, "gamma")
        img = cv2.imread(src_img_path)
        img_gamma = adjust_gamma(img, 1.5)
        img = cv2.imwrite(img_path, img_gamma)
        send = send_img_text_sticker(message, img_path, "Намного лучше, чем было 😉", "nowbetter", Filters)
        tokens['gamma'] = True
        MypyBot.register_next_step_handler(send, LetsGetWork)
    elif message.text == 'Перестань (reset brightnes)':
        send = send_img_text_sticker(message, None, "Ладно, ладно", "evil", Filters)
        tokens['gamma'] = False
        MypyBot.register_next_step_handler(send, LetsGetWork)
    else:
        try:
            gamma = (float)(message.text)
        except Exception as e:
            if flag == 0:
                send = send_img_text_sticker(message, None, "Гамма это просто число! Плохой мальчик!", "kus", baby_help_markup)
                MypyBot.register_next_step_handler(send, Gamma_Function)
                flag = 1
            else:
                send = send_img_text_sticker(message, None, "Издеваешься, да?", "cry", Filters)
                MypyBot.register_next_step_handler(send, LetsGetWork)
        if tokens.get('gamma') == False:
            src_img_path = create_save_path(message, "source")
        else:
            src_img_path = create_save_path(message, "gamma")
        img_path = create_save_path(message, "gamma")
        img = cv2.imread(src_img_path)
        img_gamma = adjust_gamma(img, gamma)
        img = cv2.imwrite(img_path, img_gamma)
        send = send_img_text_sticker(message, img_path, "О да, я даже не ожидала, что так хорошо получится", "thatsgood", Filters)
        MypyBot.register_next_step_handler(send, LetsGetWork)

@MypyBot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'yes':
                MypyBot.send_message(call.message.chat.id, 'Тогда кинь свою картинку... 😊')
                MypyBot.send_sticker(call.message.chat.id, open('Stickers/giveaphoto.webp', 'rb'))
            elif call.data == 'no':
                MypyBot.send_message(call.message.chat.id, 'Ну ничего, со всеми бывало, загружай изображение!')
                MypyBot.send_sticker(call.message.chat.id, open('Stickers/giveaphoto.webp', 'rb'))

            # elif call.data == 'minus_morojenka':
            #     MypyBot.send_message(call.message.chat.id, 'Тогда пришли мне его...')
 
            # remove inline buttons
            MypyBot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Тебе точно есть 18 ?',
                reply_markup=None)
            # MypyBot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Придется обрабатывать изображение :(",
            #     reply_markup=None)
 
            # show alert
            time.sleep(4)
            MypyBot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                            text = "Я уже заждалась твоего изображения, котик")
 
    except Exception as e:
        print(repr(e))

@MypyBot.message_handler(content_types = ['photo'])
def handle_docs_photo(message):
    try:
        file_info = MypyBot.get_file(message.photo[len(message.photo)-1].file_id)
        downloaded_img = MypyBot.download_file(file_info.file_path)
        src = create_save_path(message, "source")
        try:
            with open(src, 'wb') as saved_cup:
                saved_cup.write(downloaded_img)
        except Exception as e:
            user_images_dir = os.path.join(main_img_dir, translit(message.from_user.first_name, language_code='ru', reversed=True))
            os.mkdir(user_images_dir)
            with open(src, 'wb') as saved_cup:
                saved_cup.write(downloaded_img)
        
        send = send_img_text_sticker(message, None, "Фото добавлено, братик, без слёз не взглянешь, дайка я поработаю", "omg", Filters)
        tokens['sourse'] = True
        tokens['negative'] = False
        tokens['gamma'] = False
        tokens['gray'] = False
        tokens['sepia'] = False
        tokens['counters'] = False
        MypyBot.register_next_step_handler(send, LetsGetWork)
    except Exception as e:
        send = send_error_to_user(message, "У меня не получилось загрузить изображение, ты был слишком резок.. \n Попробуй другое 😟")
        MypyBot.register_next_step_handler(send, handle_docs_photo)

# RUN
MypyBot.polling(none_stop=True)