from dataclasses import dataclass, field
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, Table
from sqlalchemy.orm import registry


mapper_registry = registry()


@mapper_registry.mapped
@dataclass
class Article:
    __table__ = Table(
        "articles",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("handle", String),
        Column("section", String),
        Column("authors", String),
        Column("headline", String),
        Column("body", String),
        Column("source_url", String),
        Column("wordcount", Integer),
        Column("created_at", DateTime, default=datetime.utcnow),
    )

    id: int = field(init=False)
    handle: str
    section: str
    authors: str
    headline: str
    body: str
    source_url: str
    wordcount: int = None
    created_at: datetime = None
