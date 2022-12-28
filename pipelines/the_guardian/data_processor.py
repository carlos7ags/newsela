from typing import Dict, List

from prefect import flow, task

from db.models import Article


def create_article(data: Dict) -> Article:
    return Article(
        handle=data["id"],
        section=data["sectionName"],
        authors=data["fields"]["byline"],
        headline=data["fields"]["headline"],
        body=data["fields"]["body"],
        source_url=data["webUrl"],
    )


@task
def parse_data(data: List[Dict]) -> List[Article]:
    return [create_article(article) for article in data]


@flow
def process_data_flow(data: List[Dict]) -> List[Article]:
    return parse_data(data)


if __name__ == "__main__":
    process_data_flow()
