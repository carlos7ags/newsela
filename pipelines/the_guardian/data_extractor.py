import datetime
import os
from typing import Dict, List

import requests
from prefect import flow, task, get_run_logger

from pipelines.the_guardian.constants import SECTIONS_API_URL


@task
def get_sections() -> List[str]:
    """
    Get a list of the api url for each of the active sections.

    Returns:
        List[str]: a list of the api urls for active sections.
    """
    logger = get_run_logger()

    response = requests.get(SECTIONS_API_URL, params={"api-key": os.getenv("API_KEY")})
    response.raise_for_status()
    results = response.json()["response"]["results"]
    logger.info(f"Fetched {len(results)} active sections")
    return [section["apiUrl"] for section in results]


@task
def get_content(section: str) -> List[Dict]:
    """
    Get the list of articles for a given section for the current day.

    Args:
        section (str): The section id.
    Returns:
        List[Dict]: a list of articles.
    """
    logger = get_run_logger()

    params = {
        "api-key": os.getenv("API_KEY"),
        "from-date": datetime.datetime.today().strftime("%Y-%m-%d"),
        "to-date": datetime.datetime.today().strftime("%Y-%m-%d"),
        "show-fields": "headline,body,byline",
        "show-tags": "keywords",
    }
    response = requests.get(section, params=params)
    response.raise_for_status()
    results = response.json()["response"]["results"]
    logger.info(f"{len(results)} articles retrieved from {section} section")
    return results


@flow
def extract_data_flow() -> List[Dict]:
    """
    A prefect flow to get the list of articles for a given day
    from all active sections.

    Returns:
        List[Dict]: a list of articles.
    """
    results = []
    sections = get_sections()
    for section in sections:
        results += get_content(section)
    return results


if __name__ == "__main__":
    extract_data_flow()
