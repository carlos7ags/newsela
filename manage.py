import argparse
import importlib
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s",
        "--source",
        help="Name of source to execute",
        default=False,
        required=True,
    )

    args = parser.parse_args()
    module = importlib.import_module(".main_flow", package=f"pipelines.{args.source}")
    os.environ["SOURCE"] = args.source

    module.run()
