import telepot


class TelegramInterface:
    def __init__(self):
        self.token = '1412003340:AAFw5tuKKywNVCsaFg1cpCzhKihr3Vi7nbQ'
        self.bot = telepot.Bot(self.token)

    def get_bot_info(self):
        return self.bot.getMe()
