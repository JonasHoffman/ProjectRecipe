from app.schemas.telegram import TelegramUpdate


data = {
    "update_id": 123456,
    "message": {
        "message_id": 10,
        "from": {
            "id": 123,
            "first_name": "Jonas",
            "username": "jonas",
        },
        "chat": {
            "id": 123,
        },
        "voice": {
            "file_id": "AwAC123456",
            "duration": 4,
            "mime_type": "audio/ogg",
        },
    },
}


update = TelegramUpdate.model_validate(data)

print("Update ID:", update.update_id)
print("Chat ID:", update.message.chat.id)
print("Voice file ID:", update.message.voice.file_id)
print("Duration:", update.message.voice.duration)
print("Mime type:", update.message.voice.mime_type)