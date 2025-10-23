from typing import Literal

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置(支持PostgreSQL和SQLite,含连接池设置)"""
    app_name: str = "what to invest"
    debug: bool = False

    # 数据库类型
    db_type: Literal["postgres","sqlite"] = "sqlite"

    # postgresSQL数据库设置
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "postgres"
    db_password: str = "password"
    db_name: str = "what2invest"

    # 连接池配置(仅postgreSQL有效)
    pool_size: int = 20  # 连接池基础大小，数值越大越高
    max_overflow: int = 10  # 超出pool_size的最大连接数，数值越大越高
    pool_timeout: int = 30  # 获取连接超出时间，单位：秒
    pool_pre_ping: bool = True  # 连接池之前是否检查可用性

    # 可选调优参数
    pool_recycle: int = 3000  # 连接最大存活时间，单位：秒
    pool_use_info: bool = False  # 连接池取连接顺序，False=FIFO，True=LIFO 
    echo: bool = False  # 是否打印SQL，开发打开，生产关闭

    # SQLite设置
    sqlite_db_test: str = './data.what2invest.sqlite3'

    @computed_field
    @property
    def database_url(self) -> str:
        """生成数据库拼接字符串"""
        if self.db_type == 'postgres':
            return (
                f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
                f"@{self.db_host}:{self.db_port}/{self.db_name}"
            )
        elif self.db_type == "sqlite":
            return f"sqlite_aiosqlite:///{self.sqlite_db_test}"
        else:
            raise ValueError(f"Unsupported DB_TYPE: {self.db_type}")
    
    @computed_field
    @property
    def engine_options(self) -> dict:
        """统一封装数据库引擎"""
        if self.db_type == "postgres":
            return {
                "pool_size": self.pool_size,
                "max_overflow": self.max_overflow,
                "pool_timeout": self.pool_timeout,
                "pool_recycle": self.pool_recycle,
                "pool_use_info": self.pool_use_info,
                "echo": self.echo
            }
        # SQLite不支持池设置，因此返回最小参数
        return {"echo": self.echo}
    
    # JWT配置
    jwt_secret: str = "又双叒叕曼波欧码吉利曼波叮咚鸡大狗东北雨姐太带派了"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

settings = Settings()
