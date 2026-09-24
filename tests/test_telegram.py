from app.integrations.telegram.bot import TelegramBot


bot = TelegramBot()

result = bot.get_webhook_info()

print(result)