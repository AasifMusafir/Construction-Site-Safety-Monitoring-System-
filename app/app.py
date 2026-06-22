import os
import uuid
import shutil
import time
import cv2

from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from fastapi import HTTPException
from fastapi import Request

from fastapi.staticfiles import StaticFiles

from ultralytics import YOLO

from .detector import (
    InstanceDetector,
    ComplianceChecker,
    SnapshotManager
)

from .logger import CSVLogger


# ==================================
# CONFIG
# ==================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "best.pt"
)

UPLOAD_DIR = os.path.join(
    BASE_DIR,
    "uploads"
)

SNAPSHOT_DIR = os.path.join(
    BASE_DIR,
    "snapshots"
)

LOG_DIR = os.path.join(
    BASE_DIR,
    "logs"
)

CONF_THRESHOLD = 0.40

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(SNAPSHOT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)


# ==================================
# APP
# ==================================

app = FastAPI(
    title="PPE Compliance API"
)

app.mount(
    "/snapshots",
    StaticFiles(directory=SNAPSHOT_DIR),
    name="snapshots"
)

@app.get("/")
def root():
    return {
        "message": "PPE Compliance API is running",
        "docs": "/docs",
        "health": "/health"
    }

# ==================================
# LOAD MODEL
# ==================================

model = YOLO(MODEL_PATH)

instance_detector = InstanceDetector()

instance_detector.detection_mode = "multi"

compliance_checker = ComplianceChecker()

snapshot_manager = SnapshotManager(
    snapshot_dir=SNAPSHOT_DIR
)

csv_logger = CSVLogger(
    log_dir=LOG_DIR
)


# ==================================
# HELPERS
# ==================================

def convert_yolo_results(result):

    detections = []

    for box in result.boxes:

        cls_id = int(box.cls[0])

        detections.append({
            "class":
                result.names[cls_id]
        })

    return detections


# ==================================
# HEALTH
# ==================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model_loaded": True
    }


# ==================================
# PREDICT
# ==================================

@app.post("/predict")
async def predict(
    request: Request,
    file: UploadFile = File(...)
):

    if not file.content_type.startswith(
        "image/"
    ):
        raise HTTPException(
            status_code=400,
            detail="Only image files supported"
        )

    file_id = str(uuid.uuid4())[:8]

    input_path = os.path.join(
        UPLOAD_DIR,
        f"{file_id}.jpg"
    )

    with open(input_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    frame = cv2.imread(input_path)

    try:

        start = time.time()

        results = model.predict(
            source=input_path,
            conf=CONF_THRESHOLD,
            verbose=False
        )

        inference_time = round(
            (time.time() - start) * 1000,
            2
        )

        result = results[0]

        detections = convert_yolo_results(
            result
        )

        instance_result = (
            instance_detector
            .process_detection(
                detections
            )
        )

        compliant = (
            compliance_checker
            .check_compliance(
                instance_result
            )
        )

        snapshot_url = None

        if instance_result[
            "should_capture"
        ]:

            filename = (
                instance_detector
                .get_next_snapshot_filename()
            )

            snapshot_path = (
                snapshot_manager
                .save_snapshot(
                    frame,
                    filename
                )
            )

            csv_logger.log_violation(
                instance_id=
                instance_result[
                    "instance_id"
                ],
                missing_ppe=
                instance_result[
                    "missing_ppe"
                ],
                detected_ppe=
                instance_result[
                    "detected_ppe"
                ],
                snapshot_path=
                snapshot_path
            )

            snapshot_url = (
                str(request.base_url)
                + f"snapshots/{filename}.jpg"
            )

        detections_output = []

        for box in result.boxes:

            cls_id = int(box.cls[0])

            detections_output.append({

                "label":
                    result.names[cls_id],

                "confidence":
                    round(
                        float(box.conf[0]),
                        3
                    ),

                "bbox":
                    list(
                        map(
                            float,
                            box.xyxy[0]
                        )
                    )
            })

        if os.path.exists(
            input_path
        ):
            os.remove(input_path)

        return {

            "instance_id":
                instance_result[
                    "instance_id"
                ],

            "has_person":
                instance_result[
                    "has_person"
                ],

            "is_compliant":
                compliant,

            "missing_ppe":
                instance_result[
                    "missing_ppe"
                ],

            "detected_ppe":
                instance_result[
                    "detected_ppe"
                ],

            "snapshot":
                snapshot_url,

            "inference_time_ms":
                inference_time,

            "detections":
                detections_output
        }

    except Exception as e:

        if os.path.exists(
            input_path
        ):
            os.remove(input_path)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==================================
# LOGS
# ==================================

@app.get("/violations")
def violations():

    csv_file = os.path.join(
        LOG_DIR,
        "violations.csv"
    )

    if not os.path.exists(
        csv_file
    ):
        return {
            "message":
                "No violations found"
        }

    with open(
        csv_file,
        "r"
    ) as f:

        return {
            "logs":
                f.readlines()
        }