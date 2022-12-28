from datetime import datetime, timedelta

from prefect import flow

from pipelines.the_guardian.data_extractor import extract_data_flow
from pipelines.the_guardian.data_loader import load_data_flow
from pipelines.the_guardian.data_processor import process_data_flow


@flow(log_prints=True)
def main_flow() -> None:
    date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    raw_data = extract_data_flow(date)
    processed_data = process_data_flow(raw_data)
    load_data_flow(processed_data)


def run():
    main_flow()


if __name__ == "__main__":
    run()
