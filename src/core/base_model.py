from datetime import datetime,timezone

from sqlalchemy import MetaData, func, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.core.config import settings


# 约定统一的数据库命名格式，防止系统自带的metadata随意的命名数据库内的索引、约束和外键等
database_naming_convention = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey"
}

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=database_naming_convention)

# 混入类，添加创建和更新时间戳字段
class DatetimeMixin:
    # 依据不同数据库类型，设置不同的时间戳默认值和更新方式
    if settings.db_type == 'postgres':
        # postgres 支持 timezone-aware 的时间类型
        created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
            index=True
        )
        updated_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False
        )
    else:
        # 其他数据库使用应用层的时间处理
        created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            default=datetime.now(timezone.utc),
            nullable=False,
            index=True
        )
        updated_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            default=datetime.now(timezone.utc),
            onupdate=func.now(),
            nullable=False
        )
