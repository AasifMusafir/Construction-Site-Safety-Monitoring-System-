import os
import tempfile

from app.logger import CSVLogger


def test_csv_logger_creation():

    with tempfile.TemporaryDirectory() as tmp:

        logger = CSVLogger(
            log_dir=tmp
        )

        assert os.path.exists(
            logger.csv_file
        )


def test_log_entry():

    with tempfile.TemporaryDirectory() as tmp:

        logger = CSVLogger(
            log_dir=tmp
        )

        logger.log({
            "instance_id": "001",
            "is_compliant": False,
            "missing_ppe": ["helmet"]
        })

        assert os.path.exists(
            logger.csv_file
        )

        with open(
            logger.csv_file,
            "r"
        ) as f:

            content = f.read()

        assert "001" in content