from typing import List, Dict
from prefect import task, flow


@task
def get_sections() -> List[str]:
    pass


@task
def get_content(section: str) -> List[str]:
    pass


@flow
def extract_data_flow() -> List[Dict]:
    pass


if __name__ == "__main__":
    extract_data_flow()
