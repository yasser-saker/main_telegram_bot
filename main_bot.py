import telebot
from datetime import datetime
import json
from random import choice


class MainBot:
    def __init__(self, BOT_TOKEN, default_lang="ar"):
        self.BOT_TOKEN = BOT_TOKEN
        self.bot = telebot.TeleBot(self.BOT_TOKEN)
        self.default_lang = default_lang


class ReadingWriting:
    def __init__(self, texting_static_file="texting_static.json", texting_random_file="texting_random.json", data_file="data.json", commands_file="commands.json"):
        self.texting_static_file = texting_static_file
        self.texting_random_file = texting_random_file
        self.data_file = data_file
        self.commands_file = commands_file
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


class MessageInfo:
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


class Dealing(ReadingWriting):
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


class DateTime:
    def __init__(self, datetime_format="%Y-%m-%d %H:%M:%S"):
        self.datetime_format = datetime_format

    def time_date_now(self):  # get time now
        date = datetime.now()
        date_string = date.strftime(self.datetime_format)
        return date_string

    def date_now(self):
        return self.time_date_now()[0: self.time_date_now().index(" ")]

    def date_of_time_date(self, time_date):
        return time_date[0: time_date.index(" ")]

    def year_now(self):
        return self.date_now()[0:self.date_now().index("-")]

    def month_now(self):
        return self.date_now()[self.date_now().index("-")+1:self.date_now().index("-", self.date_now().index("-")+1)]

    def day_now(self):
        return self.date_now()[self.date_now().index("-", self.date_now().index("-")+1)+1:]

    def year_of_date(self, date):
        return date[0:date.index("-")]

    def month_of_date(self, date):
        return date[date.index("-")+1:date.index("-", date.index("-")+1)]

    def day_of_date(self, date):
        return date[date.index("-", date.index("-")+1)+1:]

    def time_now(self):
        return self.time_date_now()[self.time_date_now().index(" ")+1:]

    def time_of_time_date(self, time_date):
        return time_date[time_date.index(" ")+1:]

    def hours_now(self):
        return self.time_now()[0: self.time_now().index(":")]

    def minutes_now(self):
        return self.time_now()[self.time_now().index(":")+1: self.time_now().index(":", self.time_now().index(":")+1)]

    def seconds_now(self):
        return self.time_now()[self.time_now().index(":", self.time_now().index(":")+1)+1:]

    def hours_of_time(self, time):
        return time[0: time.index(":")]

    def minutes_of_time(self, time):
        return time[self.time_now().index(":")+1: time.index(":", time.index(":")+1)]

    def seconds_of_time(self, time):
        return time[time.index(":", time.index(":")+1)+1:]

    def calculate_date_difference(self, date1, date2, date_format="%Y-%m-%d"):
        date1 = datetime.strptime(date1, date_format)
        date2 = datetime.strptime(date2, date_format)
        difference = date2 - date1
        return difference.days

    def calculate_time_difference(self, time1, time2, time_format="%H:%M:%S"):
        time1 = datetime.strptime(time1, time_format)
        time2 = datetime.strptime(time2, time_format)
        difference = time2 - time1
        return difference

    def calculate_datetime_difference(self, datetime1, datetime2, datetime_format="%Y-%m-%d %H:%M:%S"):
        datetime1 = datetime.strptime(datetime1, datetime_format)
        datetime2 = datetime.strptime(datetime2, datetime_format)

        difference = datetime2 - datetime1

        return difference

    def calculate_datetime_difference_in_days(self, datetime1, datetime2, datetime_format="%Y-%m-%d %H:%M:%S"):
        datetime1 = datetime.strptime(datetime1, datetime_format)
        datetime2 = datetime.strptime(datetime2, datetime_format)
        difference = datetime2 - datetime1
        return difference.days

    def gap_now_and_date(self, date, date_format="%Y-%m-%d"):
        return self.calculate_date_difference(date, self.date_now(), date_format)

    def gap_now_and_time(self, time, time_format="%H:%M:%S"):
        return self.calculate_time_difference(time, self.time_now(), time_format)

    def gap_now_and_timedate(self, datetime, datetime_format="%Y-%m-%d %H:%M:%S"):
        return self.calculate_datetime_difference(datetime, self.time_date_now(), datetime_format)

    def gap_now_and_timedate_in_days(self, datetime, datetime_format="%Y-%m-%d %H:%M:%S"):
        return self.calculate_datetime_difference(datetime, self.time_date_now(), datetime_format).days


class Users:
    def __init__(self, data_file="data.json", default_lang="ar"):
        self.data_file = data_file
        self.default_lang = default_lang
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
        try:
            return self.get_user(message)["lang"]
        except:
            return self.default_lang

    def change_lang(self, message, new_lang):
        self.edit_info(message, "lang", new_lang)


class Bot(MainBot, Dealing, Users, DateTime, MessageInfo, ReadingWriting):
    def __init__(self, BOT_TOKEN, default_lang="ar", datetime_format="%Y-%m-%d %H:%M:%S", texting_static_file="texting_static.json", texting_random_file="texting_random.json", data_file="data.json", commands_file="commands.json"):
        MainBot.__init__(self, BOT_TOKEN, default_lang)
        ReadingWriting.__init__(self, texting_static_file,
                                texting_random_file, data_file, commands_file)
        DateTime.__init__(self, datetime_format)
        self.bot = telebot.TeleBot(self.BOT_TOKEN)

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
                self.bot.send_message(
                    message.chat.id, self.deal_commands("help", self.default_lang))

        # change lang to arabic handler
        @self.bot.message_handler(commands=["ar"])
        def arabicBot(message):
            if self.check_user_exists(message):
                self.bot.send_message(
                    message.chat.id, self.deal_commands("ar", self.get_lang(message)))
                self.edit_info(message, "lang", "ar")
            else:
                self.bot.send_message(
                    message.chat.id, self.deal_commands("ar", self.default_lang))
                self.edit_info(message, "lang", "ar")

        # change lang to english handler
        @self.bot.message_handler(commands=["en"])
        def englishBot(message):
            if self.check_user_exists(message):
                self.bot.send_message(message.chat.id, self.deal_commands(
                    "en", self.get_lang(message)))
                self.edit_info(message, "lang", "en")
            else:
                self.bot.send_message(message.chat.id, self.deal_commands(
                    "en", self.default_lang))
                self.edit_info(message, "lang", "en")

        @self.bot.message_handler(commands=["end"])  # delete handler
        def deleteBot(message):
            if self.check_user_exists(message):
                self.bot.send_message(message.chat.id, self.deal_commands(
                    "end", self.get_lang(message)))
                self.delete_user(message)
            else:
                self.bot.send_message(message.chat.id, self.deal_commands(
                    "end", self.default_lang))
