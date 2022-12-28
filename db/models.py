from dataclasses import field
from pydantic.dataclasses import dataclass

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Table
from sqlalchemy.orm import registry

mapper_registry = registry()


@mapper_registry.mapped
@dataclass
class Article:
    """
    An Article entity (dataclass).
    """

    __table__ = Table(
        "articles",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("source", String),
        Column("handle", String, unique=True),
        Column("section", String),
        Column("authors", String),
        Column("headline", String),
        Column("body", String),
        Column("source_url", String),
        Column("wordcount", Integer),
        Column("created_at", DateTime, default=datetime.utcnow),
    )

    source: str
    handle: str
    section: str
    authors: str
    headline: str
    body: str
    source_url: str
    id: int = None
    wordcount: int = None
    created_at: datetime = None

    def __eq__(self, other):
        if self.id is None or other.id is None:
            return self.handle == other.handle
        else:
            return self.id == other.id

    def __hash__(self):
        return hash(self.handle)
