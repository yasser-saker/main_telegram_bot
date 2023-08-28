import telebot
import json
from random import choice
from server import server


class Bot:
    def __init__(self, BOT_TOKEN, time_format="%Y-%m-%d %H:%M:%S", commands_file="commands.json", data_file="data.json", texting_static_file="texting_static.json", texting_random_file="texting_random.json", default_lang="ar"):
        self.BOT_TOKEN = BOT_TOKEN
        self.time_format = time_format
        self.bot = telebot.TeleBot(self.BOT_TOKEN)
        self.commands_file = commands_file
        self.data_file = data_file
        self.texting_static_file = texting_static_file
        self.texting_random_file = texting_random_file
        self.default_lang = default_lang

        @self.bot.message_handler(commands=["start"])  # start handler
        def startBot(message):
            self.bot.send_message(
                message.chat.id, self.deal_commands("start", self.default_lang))
            self.add_user(message)

        @self.bot.message_handler(commands=["help"])  # help handler
        def helpBot(message):
            if self.check_user_exists(message):
                self.bot.send_message(
                    message.chat.id, self.deal_commands("help", self.get_lang(message)))
            else:
                self.bot.send_message(message.chat.id, self.deal_commands(
                    "not_user", self.get_lang(message)))

        # change lang to arabic handler
        @self.bot.message_handler(commands=["ar"])
        def arabicBot(message):
            if self.check_user_exists(message):
                self.bot.send_message(
                    message.chat.id, self.deal_commands("ar", self.get_lang(message)))
                self.edit_info(message, "lang", "ar")
            else:
                self.bot.send_message(message.chat.id, self.deal_commands(
                    "not_user", self.get_lang(message)))

        # change lang to english handler
        @self.bot.message_handler(commands=["en"])
        def englishBot(message):
            if self.check_user_exists(message):
                self.bot.send_message(message.chat.id, self.deal_commands(
                    "en", self.get_lang(message)))
                self.edit_info(message, "lang", "en")
            else:
                self.bot.send_message(message.chat.id, self.deal_commands(
                    "not_user", self.get_lang(message)))

        @self.bot.message_handler(commands=["end"])  # delete handler
        def deleteBot(message):
            if self.check_user_exists(message):
                self.bot.send_message(message.chat.id, self.deal_commands(
                    "end", self.get_lang(message)))
                self.delete_user(message)
            else:
                self.bot.send_message(message.chat.id, self.deal_commands(
                    "no_end", self.get_lang(message)))

    # Reading And Writing On Files

    def reading(self, file_name):  # reading data from json file
        with open(file_name, "r", encoding="utf-8") as fileRead:
            data = json.load(fileRead)
        return data

    def writing(self, file_name, new_data):  # writing new data on json file
        with open(file_name, 'w') as fileWrite:
            json.dump(new_data, fileWrite, indent=4)

    def reading_data(self):
        return self.reading(self.data_file)

    def reading_commands(self):
        return self.reading(self.commands_file)

    def reading_texting_static(self):
        return self.reading(self.texting_static_file)

    def reading_texting_random(self):
        return self.reading(self.texting_random_file)

    def writing_data(self, data):
        self.writing(self.data_file, data)

    # Deal Messages And Commands
    def deal_commands(self, command, lang):
        data = self.reading_commands()
        return data[lang][command]

    def deal_messages(self, message, lang):
        data_random = self.reading_texting_random()
        data_static = self.reading_texting_static()
        for category in data_random:
            if (message in data_random[category][0]):
                return choice(data_random[category][1])
        if message in data_static:
            return data_static[message]
        else:
            return self.deal_commands("unknown", lang)

    # Get Informations Of User
    def user_id(self, message):  # get id of a user
        return str(message.from_user.id)

    def user_first_name(self, message):  # get first name of a user
        return message.from_user.first_name

    def user_last_name(self, message):  # get last name of a user
        if message.from_user.last_name != None:
            return message.from_user.last_name
        else:
            return ""

    def user_full_name(self, message):  # get full name of a user
        if self.user_last_name != None:
            return self.user_first_name(message) + self.user_last_name(message)
        else:
            return self.user_first_name(message)

    def user_username(self, message):  # get username of a user
        return str(message.from_user.username)

    # Dealing With Users Data In Database
    def deal_data_file(self):
        data = self.reading_data()
        if data == "":
            data = {"users": {}}
        elif "users" not in data:
            data = {"users": {}}
        self.writing_data(data)

    def add_user(self, message):
        data = self.reading_data()
        if "users" not in data:
            data = {"users": {}}
        users = data["users"]
        if self.user_id(message) not in users:
            users[self.user_id(message)] = {}
            users[self.user_id(message)]["Name"] = self.user_full_name(message)
            users[self.user_id(message)]["Username"] = self.user_username(
                message)
            users[self.user_id(message)]["lang"] = self.default_lang
        self.writing_data(data)

    def check_user_exists(self, message):
        data = self.reading_data()
        self.deal_data_file()
        users = data["users"]
        return self.user_id(message) in users

    def get_user(self, message):
        if self.check_user_exists(message):
            data = self.reading_data()
            self.deal_data_file()
            users = data["users"]
            return users[self.user_id(message)]

    def update_user(self, message):
        data = self.reading_data()
        self.deal_data_file()
        users = data["users"]
        users[self.user_id(message)]["Name"] = self.user_full_name(message)
        users[self.user_id(message)]["Username"] = self.user_username(message)

    def reset_user(self, message):
        data = self.reading_data()
        self.deal_data_file()
        users = data["users"]
        users[self.user_id(message)] = {}
        users[self.user_id(message)]["Name"] = self.user_full_name(message)
        users[self.user_id(message)]["Username"] = self.user_username(message)
        users[self.user_id(message)]["lang"] = self.default_lang
        self.writing_data(data)

    def delete_user(self, message):
        data = self.reading_data()
        self.deal_data_file()
        users = data["users"]

        if users[self.user_id(message)]:
            users.pop(self.user_id(message))
        self.writing_data(data)

    def add_info(self, message, info, value):
        data = self.reading_data()
        self.deal_data_file()
        users = data["users"]
        users[self.user_id(message)][info] = value
        self.writing_data(data)

    def check_info(self, message, info):
        data = self.reading_data()
        self.deal_data_file()
        users = data["users"]
        return info in users[self.user_id(message)]

    def get_info(self, message, info):
        data = self.reading_data()
        self.deal_data_file()
        users = data["users"]
        info = users[self.user_id(message)][info]
        return info

    def edit_info(self, message, info, value):
        data = self.reading_data()
        self.deal_data_file()
        users = data["users"]
        users[self.user_id(message)][info] = value
        self.writing_data(data)

    def delete_info(self, message, info):
        data = self.reading_data()
        self.deal_data_file()
        users = data["users"]
        if users[self.user_id(message)][info]:
            users[self.user_id(message)].pop(info)
        self.writing_data(data)

    # Get Some Specific Details About User
    def get_lang(self, message):
        return self.get_user(message)["lang"]

    def change_lang(self, message, new_lang):
        self.edit_info(message, "lang", new_lang)


# BOT_NAME = Bot("(BOT_TOKEN)")
# server()
# print('Bot Started..')
# BOT_NAME.bot.infinity_polling()
