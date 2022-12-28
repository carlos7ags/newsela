from typing import List

from prefect import flow, task

from db.db_manager import DatabaseManager
from db.models import Article


@task
def load_data_to_db(data: List[Article]) -> None:
    """
    Insert or update articles into the database.

    Args:
        data (List[Article]): A list of Articles.
    """
    db_manager = DatabaseManager[Article](Article)
    db_manager.upsert_items(data)


@flow
def load_data_flow(data: List[Article]) -> None:
    """
    A flow to handle the persistence of processed Articles.
    """
    load_data_to_db(data)
