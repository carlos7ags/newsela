import os
from dataclasses import asdict
from typing import Any, Dict, Generic, List, Optional, TypeVar

from prefect import get_run_logger
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

# logger = get_run_logger()

T = TypeVar("T")


class DatabaseManager(Generic[T]):
    """
    Concentrates operations with the database with a simplified interface.
    The generic placeholder corresponds to a data model.
    """

    def __init__(
        self,
        data_model: T,
        host: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
    ):

        self.session = None
        self.data_model = data_model
        self.host = host if host else os.getenv("POSTGRES_HOST")
        self.username = username if username else os.getenv("POSTGRES_USER")
        self.password = password if password else os.getenv("POSTGRES_PASSWORD")
        self.database = database if database else os.getenv("POSTGRES_DBNAME")

        self.engine = create_engine(
            f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}/{self.database}",
            echo=False,
        )
        self.Session = sessionmaker(bind=self.engine)
        self._create_table()

    def _create_table(self) -> None:
        """
        Creates a table for the data model in the database if it does not exist.
        """
        table_name = self.data_model.__table__.name
        if not inspect(self.engine).has_table(table_name):
            self.data_model.__table__.create(bind=self.engine, checkfirst=True)
            print(f"Table {table_name} created")
        else:
            print(f"Table {table_name} already in database")

    def bulk_insert_items(self, data: List[T]) -> None:
        """
        Insert a list of items into the database.

        Args:
            data (List[T]): A list of data objects.
        """
        with self.Session.begin() as session:
            session.bulk_save_objects(data, update_changed_only=False)
            print(
                f"{len(data)} elements successfully created in {self.data_model.__table__.name}"
            )

    def upsert_items(self, items: List[T], key: str = "id") -> None:
        """
        Inserts a list of objects into the data model table if new,
        or updates the objects if already exists in the database.

        Args:
            items (List[T]): A list of data objects.
            key (str): The unique field to use as primary key.
        """
        new_items = []
        for item in items:
            filter_by = {key: item.__getattribute__(key)}
            if not self.item_exist(filter_by):
                new_items.append(item)
            else:
                self.update_item_by(item, filter_by)
        if new_items:
            self.bulk_insert_items(new_items)
        print(
            f"{len(items)} elements successfully updated/created in {self.data_model.__table__.name}"
        )

    def get_item_by(self, filter_by: Dict[str, Any]) -> Optional[T]:
        """
        Retrieve an item from the database based on filter parameters (returns first match).

        Args:
            filter_by (Dict[str, Any]): A dictionary containing the parameters and values to filter by.
        Returns:
            Optional[T]: The matching data object if exists.
        """
        with self.Session.begin() as session:
            item = session.query(self.data_model).filter_by(**filter_by).first()
            session.expunge(item)
            return item

    def item_exist(self, filter_by: Dict[str, Any]) -> bool:
        """
        Verify if an object exists in the database based on filter parameters.

        Args:
            filter_by (Dict[str, Any]): A dictionary containing the parameters and values to filter by.
        Returns:
            bool: A boolean representing if the object exists.
        """
        with self.Session.begin() as session:
            return bool(session.query(self.data_model).filter_by(**filter_by).first())

    def update_item_by(self, item: T, filter_by: Dict[str, Any]) -> None:
        """
        Update the fields values of an existing item in the database (updated the first match for non-unique fields).

        Args:
            item (T): The updated item.
            filter_by (Dict[str, Any]): A dictionary containing the parameters and values to filter by.
        """
        with self.Session.begin() as session:
            session.query(self.data_model).filter_by(**filter_by).update(
                asdict(
                    item, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}
                ),
                synchronize_session="fetch",
            )
