import os
from typing import Dict, List

from prefect import flow, task

from db.models import Article


def create_article(data: Dict) -> Article:
    return Article(
        source=os.getenv("SOURCE"),
        handle=data["id"],
        section=data["sectionName"],
        authors=data["fields"]["byline"],
        headline=data["fields"]["headline"],
        body=data["fields"]["body"],
        source_url=data["webUrl"],
    )


@task
def delete_duplicates(data: List[Article]) -> List[Article]:
    return list(set(data))


@task
def parse_data(data: List[Dict]) -> List[Article]:
    return [create_article(article) for article in data]


@flow
def process_data_flow(data: List[Dict]) -> List[Article]:
    data = parse_data(data)
    data = delete_duplicates(data)
    return data


if __name__ == "__main__":
    process_data_flow()
