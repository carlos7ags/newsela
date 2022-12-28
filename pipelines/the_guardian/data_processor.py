import os
import re
from typing import Any, Dict, List

from prefect import flow, task

from db.models import Article


def create_article(data: Dict[str, Any]) -> Article:
    """
    Create an Article entity from a dict.

    Args:
        data (Dict[str, Any]): A dictionary containing the article fields.
    Returns:
        Article: An Article entity.
    """
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
def remove_html_tags(article: Article) -> Article:
    clean_html = re.compile('<.*?>')
    article.body = re.sub(clean_html, "", article.body)
    article.headline = re.sub(clean_html, "", article.headline)
    return article


@task
def set_wordcount(article: Article) -> Article:
    article.wordcount = len(article.body)
    return article


@task
def delete_duplicates(data: List[Article]) -> List[Article]:
    """
    Removes duplicate entries of an Article entity.

    Args:
        data (List[Article]): A list of Article entities.
    Returns:
        List[Article]: A list of Article entities.
    """
    return list(set(data))


@task
def parse_data(data: List[Dict]) -> List[Article]:
    return [create_article(article) for article in data]


@flow
def process_data_flow(data: List[Dict]) -> List[Article]:
    data = parse_data(data)
    data = delete_duplicates(data)
    data = [remove_html_tags(article) for article in data]
    data = [set_wordcount(article) for article in data]
    return data


if __name__ == "__main__":
    process_data_flow()
