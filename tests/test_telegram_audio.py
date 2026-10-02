from app.integrations.telegram.bot import TelegramBot


bot = TelegramBot()

file_id = input("Enter the Telegram audio file_id: ")

file_info = bot.get_file(file_id)

print("File info:")
print(file_info)

file_path = file_info["result"]["file_path"]

destination = "audio.ogg"

bot.download_file(
    file_path,
    destination,
)

print(f"Audio downloaded to: {destination}")