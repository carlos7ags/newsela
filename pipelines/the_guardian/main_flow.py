import os

from prefect import flow
from .data_extractor import extract_data_flow


@flow
def main_flow() -> None:
    raw_data = extract_data_flow()


def run():
    main_flow()


if __name__ == "__main__":
    run()
