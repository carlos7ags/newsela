import os

from prefect import flow

from pipelines.the_guardian.data_extractor import extract_data_flow
from pipelines.the_guardian.data_loader import load_data_flow
from pipelines.the_guardian.data_processor import process_data_flow


@flow
def main_flow() -> None:
    raw_data = extract_data_flow()
    processed_data = process_data_flow(raw_data)
    load_data_flow(processed_data)


def run():
    main_flow()


if __name__ == "__main__":
    run()
