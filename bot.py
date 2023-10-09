

import telebot

bot = telebot.TeleBot("6694663855:AAHL7RYBLDQNHlxsjskXtYEg_saGZUoqnU0")


bot.set_my_commands([
    telebot.types.BotCommand("/start","Начать"),
    telebot.types.BotCommand("/inf","Информатика"),
    telebot.types.BotCommand("/help","Иструкции по использлванию"),
    telebot.types.BotCommand("/about","О нас"),
])



# Создаем словарь, в котором будем хранить импорты для каждого пользователя
user_imports = {}
user_imports2 = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name
    text = f"Привет, {user_name}.\n\nЯ бот, который позволит тебе легко узнавать ответы на твой тест на платоне.\nЧтобы продолжить использование бота введите /inf\n\nСсылка на"
    url="<a href='https://platon.s1212.ru/'>сайт</a>"
    bot.send_message(message.chat.id, text+" "+url,parse_mode="HTML")

@bot.message_handler(commands=['import'])
def import_text(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Отправь текст, который является отличительной особенностью задачи не используйте символы (например такие особенности могут быть в кавычках или назавания чего либо)")
    bot.register_next_step_handler(message, process_import)

@bot.message_handler(commands=['number'])
def input_number(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Введите номер выбраной задачи")
    bot.register_next_step_handler(message, process_number)

def process_number(message):
    user_id = message.from_user.id
    user_imports2[user_id] = message.text

    # Путь к файлу
    путь_к_файлу = 'answers3.txt'

    # Искомое число
    искомое_число = message.text

    # Попытка открыть файл и выполнить поиск
    try:
        with open(путь_к_файлу, 'r') as файл:
            found = False
            for строка in файл:
                if f"[{искомое_число}]" in строка:
                    bot.send_message(user_id, строка)
                    found = True
                    break
            if not found:
                bot.send_message(user_id, f"Искомое число '{искомое_число}' не найдено в файле.")
    except FileNotFoundError:
        bot.send_message(user_id, f"Файл '{путь_к_файлу}' не найден.")


@bot.message_handler(commands=['about'])
def about(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Проект создан одним интузиастом я могу быть среди вас..\n\nКонечно же вы можете использовать ответы бота в своих целях")

@bot.message_handler(commands=['inf'])
def inf(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "На данный момент доступно решение задания №3\n\nВведите это /import чтобы ввести свою задачу.")

def process_import(message):
    user_id = message.from_user.id
    user_imports[user_id] = message.text
    bot.send_message(user_id, "Текст успешно записан. Чтобы найти задачу отправьте /search")

@bot.message_handler(commands=['search'])
def search_text(message):
    user_id = message.from_user.id
    if user_id in user_imports:
        imported_text = user_imports[user_id]

        # Открываем файл для чтения и выполняем поиск
        try:
            with open('ege3.txt', 'r', encoding='utf-8') as file:
                found_mertvye_dushi = False
                for line in file:
                    if imported_text in line:
                        found_mertvye_dushi = True
                        bot.send_message(user_id, line)
                    elif found_mertvye_dushi and line.strip() == "":
                        break
                    elif found_mertvye_dushi:
                        bot.send_message(user_id, line)
                bot.send_message(user_id, "🥳 Задание найдено! Выберите из предложеных задач вашу и напишите её номер. Так же убедитесь что это именно ваша задача\n\nОтправь /number а затем введи номер задания")

        except FileNotFoundError:
            bot.send_message(user_id, f"Не удалось получить доступ к базе с заданиями")
    else:
        bot.send_message(user_id, "Сначала импортируй текст с помощью команды /import")

bot.infinity_polling()
