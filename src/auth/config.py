from pydantic_settings import BaseSettings,SettingsConfigDict


class AuthSettings(BaseSettings):
    """认证模块专属配置"""

    jwt_secret: str = "SAY_MY_NAME_BETTER_CALL_SAUL"

    model_config = SettingsConfigDict(
        env_file=".env.auth",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

auth_settings = AuthSettings()
