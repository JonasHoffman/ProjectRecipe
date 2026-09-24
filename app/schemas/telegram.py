from pydantic import BaseModel,ConfigDict, Field



class TelegramUser(BaseModel):
    id: int
    first_name: str | None = None
    username: str | None = None


class TelegramChat(BaseModel):
    id: int


class TelegramMessage(BaseModel):
    message_id: int
    from_: TelegramUser | None = Field(
        default=None,
        alias="from",
    )
    chat: TelegramChat
    text: str | None = None

    model_config = ConfigDict(
        populate_by_name=True,
    )



class TelegramUpdate(BaseModel):
    update_id: int
    message: TelegramMessage | None = None