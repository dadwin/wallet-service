from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime

from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime
from datetime import datetime


# https://docs.sqlalchemy.org/en/14/core/compiler.html#further-examples
class utcnow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class CreatedAtMixin:
    created_at = Column(DateTime, default=datetime.utcnow())


class UpdatedAtMixin:
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow)


class TrackTimeMixin(CreatedAtMixin, UpdatedAtMixin):
    pass


class SoftDeleteMixin:
    deleted_at = Column(DateTime, nullable=True)
