# multicam_ppe.py

import cv2
import time
import threading
import logging
from datetime import datetime

from ultralytics import YOLO

from ..detector import (
    InstanceDetector,
    ComplianceChecker,
    SnapshotManager
)

from logger import CSVLogger


# CAMERA WORKER
class PPECameraDetector:

    def __init__(
        self,
        camera_name,
        source,
        model,
        snapshot_manager,
        csv_logger
    ):

        self.camera_name = camera_name
        self.source = source

        self.model = model

        self.snapshot_manager = snapshot_manager
        self.csv_logger = csv_logger

        self.instance_detector = InstanceDetector()
        self.compliance_checker = ComplianceChecker()

        self.running = False
        self.thread = None
        self.cap = None

        self.latest_result = {}

        self.logger = logging.getLogger(camera_name)
        self.logger.setLevel(logging.INFO)
  
    # CAMERA INIT

    def initialize_camera(self):

        self.cap = cv2.VideoCapture(self.source)

        if not self.cap.isOpened():

            self.logger.error(
                f"{self.camera_name}: Failed to connect"
            )

            return False

        return True

    # RECONNECT

    def reconnect(self):

        self.logger.warning(
            f"{self.camera_name}: Reconnecting..."
        )

        if self.cap:
            self.cap.release()

        time.sleep(2)

        return self.initialize_camera()

    # YOLO DETECTIONS

    def run_inference(self, frame):

        result = self.model(
            frame,
            conf=0.4,
            verbose=False
        )[0]

        detections = []

        for box in result.boxes:

            cls_id = int(box.cls[0])

            conf = float(box.conf[0])

            x1, y1, x2, y2 = map(
                float,
                box.xyxy[0]
            )

            detections.append({
                "class":
                    result.names[cls_id],

                "confidence":
                    round(conf, 3),

                "bbox":
                    [x1, y1, x2, y2]
            })

        return result, detections

    # FRAME PROCESSING

    def process_frame(self, frame):

        start = time.time()

        result, detections = self.run_inference(frame)

        instance_result = (
            self.instance_detector
            .process_detection(detections)
        )

        snapshot_path = None

        if instance_result["should_capture"]:

            filename = (
                self.instance_detector
                .get_next_snapshot_filename()
            )

            annotated = result.plot()

            snapshot_path = (
                self.snapshot_manager
                .save_snapshot(
                    annotated,
                    filename
                )
            )

        inference_ms = round(
            (time.time() - start) * 1000,
            2
        )

        response = {

            "camera":
                self.camera_name,

            "timestamp":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "instance_id":
                instance_result["instance_id"],

            "has_person":
                instance_result["has_person"],

            "is_compliant":
                instance_result["is_compliant"],

            "missing_ppe":
                instance_result["missing_ppe"],

            "detected_ppe":
                instance_result["detected_ppe"],

            "snapshot":
                snapshot_path,

            "inference_time_ms":
                inference_ms,

            "detections":
                detections
        }

        self.latest_result = response

        self.csv_logger.log(response)

        return response

    # MAIN LOOP

    def run(self):

        if not self.initialize_camera():
            return

        self.running = True

        while self.running:

            ret, frame = self.cap.read()

            if not ret:

                self.logger.warning(
                    f"{self.camera_name}: Frame read failed"
                )

                if not self.reconnect():
                    continue

            try:

                response = self.process_frame(frame)

                print(
                    f"[{self.camera_name}] "
                    f"Compliance: "
                    f"{response['is_compliant']}"
                )

            except Exception as e:

                self.logger.exception(str(e))

            time.sleep(0.01)

        self.cap.release()

    # START / STOP

    def start(self):

        self.thread = threading.Thread(
            target=self.run,
            daemon=True
        )

        self.thread.start()

    def stop(self):

        self.running = False


# MULTI CAMERA MANAGER

class MultiCameraManager:

    def __init__(self, model_path):

        self.model = YOLO(model_path)

        self.snapshot_manager = SnapshotManager(
            "snapshots"
        )

        self.csv_logger = CSVLogger(
            "logs"
        )

        self.cameras = {}

    def add_camera(
        self,
        camera_name,
        source
    ):

        detector = PPECameraDetector(

            camera_name=camera_name,

            source=source,

            model=self.model,

            snapshot_manager=
                self.snapshot_manager,

            csv_logger=
                self.csv_logger
        )

        self.cameras[camera_name] = detector

    def start_all(self):

        for camera in self.cameras.values():

            camera.start()

    def stop_all(self):

        for camera in self.cameras.values():

            camera.stop()

    def get_status(self):

        return {

            name:
                cam.latest_result

            for name, cam
            in self.cameras.items()
        }


# MAIN

if __name__ == "__main__":

    manager = MultiCameraManager(
        model_path="best.pt"
    )

    manager.add_camera(
        "Cam_1",
        "rtsp://camera1"
    )

    manager.add_camera(
        "Cam_2",
        "rtsp://camera2"
    )

    manager.add_camera(
        "Cam_3",
        "rtsp://camera3"
    )

    manager.start_all()

    try:

        while True:

            time.sleep(5)

            print(
                manager.get_status()
            )

    except KeyboardInterrupt:

        manager.stop_all()