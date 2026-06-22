import csv
import os
from datetime import datetime


class CSVLogger:

    def __init__(self, log_dir="logs"):
        os.makedirs(log_dir, exist_ok=True)

        self.csv_file = os.path.join(
            log_dir,
            "violations.csv"
        )

        if not os.path.exists(self.csv_file):

            with open(self.csv_file, "w", newline="") as f:

                writer = csv.writer(f)

                writer.writerow([
                    "timestamp",
                    "instance_id",
                    "status",
                    "missing_ppe",
                    "detected_ppe",
                    "snapshot_path"
                ])

    def log_violation(
        self,
        instance_id,
        missing_ppe,
        detected_ppe,
        snapshot_path
    ):

        with open(self.csv_file, "a", newline="") as f:

            writer = csv.writer(f)

            writer.writerow([
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                instance_id,
                "NON_COMPLIANT",
                ",".join(missing_ppe),
                ",".join(detected_ppe),
                snapshot_path
            ])