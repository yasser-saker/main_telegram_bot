from main_bot import *


class NewBot(Bot):
    def __init__(self, BOT_TOKEN, default_lang="ar", datetime_format="%Y-%m-%d %H:%M:%S", texting_static_file="texting_static.json", texting_random_file="texting_random.json", data_file="data.json", commands_file="commands.json"):
        super().__init__(BOT_TOKEN, default_lang, datetime_format,
                         texting_static_file, texting_random_file, data_file, commands_file)
        # Continue Your Bot Code Here


newbot = NewBot("TYPE YOUR TOKEN HERE..")
print('Bot Started..')
newbot.bot.infinity_polling()
