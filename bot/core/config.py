import re

from pydantic import BaseSettings, validator


class Channels(BaseSettings):
    """Channel ids."""

    devlog: int = 0

    @validator("devlog")
    def check_ids_format(cls, v: list[int]) -> list[int]:
        """Validate discord ids format."""
        if not v:
            return v

        assert len(str(v)) == 18, "Discord ids must have a length of 18."
        return v

    class Config:
        """The Pydantic settings configuration."""

        env_file = ".env"
        env_prefix = "CHANNEL_"


class Chat(BaseSettings):
    """Chat gpt config."""

    session: str
    email: str = ""
    password: str = ""

    class Config:
        """The Pydantic settings configuration."""

        env_file = ".env"
        env_prefix = "GPT_"


class Client(BaseSettings):
    """The API settings."""

    name: str = "Bot"
    token: str

    class Config:
        """The Pydantic settings configuration."""

        env_file = ".env"
        env_prefix = "BOT_"


class Roles(BaseSettings):
    """The roles settings."""

    admin: str = "Admin"
    everyone: str = "@everyone"

    class Config:
        """The Pydantic settings configuration."""

        env_file = ".env"
        env_prefix = "ROLE_"


class Global(BaseSettings):
    """The app settings."""

    client: Client = Client()
    channels: Channels = Channels()
    chat: Chat = Chat()
    roles: Roles = Roles()

    dev_guild_ids: list[int] = []
    guild_ids: list[int]

    debug: bool = False

    @validator("guild_ids", "dev_guild_ids")
    def check_ids_format(cls, v: list[int]) -> list[int]:
        """Validate discord ids format."""
        for discord_id in v:
            assert len(str(discord_id)) == 18, "Discord ids must have a length of 18."
        return v

    class Config:
        """The Pydantic settings configuration."""

        env_file = ".env"


settings = Global()
