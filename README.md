# PPE Compliance Monitoring System

A real-time Personal Protective Equipment (PPE) compliance monitoring system built using YOLO, FastAPI, and OpenCV. The system detects workers, verifies PPE compliance, logs violations, captures evidence snapshots, and supports multi-camera RTSP streams.

---

# Features

- YOLO-based PPE Detection
- Real-time inference
- FastAPI REST API
- Multi-camera RTSP support
- PPE compliance validation
- Violation tracking
- Snapshot capture for violations
- CSV-based logging
- Swagger UI documentation
- Extensible for industrial deployments

---

# Dataset Research and Selection : **https://github.com/AasifMusafir/Construction-Site-Safety-Monitoring-System-/blob/main/training/notebook/README.md**

# Project Structure

```text
PPE_Detector/
│
├── app/
│   ├── app.py
│   ├── detector.py
│   ├── logger.py
│   ├── __init__.py
│   │
│   ├── cameras/
│   │   ├── multi_cam_rtsp.py
│   │   └── __init__.py
│   │
│   ├── uploads/
│   ├── snapshots/
│   ├── logs/
│   └── model/
        └── tensorrt
        │  └── best.onnx
        └── tflite
        |  └── best_float32.tflite
        └── best.pt
│
├── tests/
│   ├── test_detector.py
│   ├── test_logger.py
│   ├── test_camera.py
│   └── test_api.py
│
├── configs/
│   └── config.yaml
│
├── notebooks/
│   └── train.ipynb
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# System Requirements

## Hardware

Recommended:

- Intel i5 / i7 or equivalent
- 8 GB RAM minimum
- NVIDIA GPU (optional but recommended)

## Software

- Python 3.9+
- OpenCV
- FastAPI
- Uvicorn
- Ultralytics YOLO

---

# Installation

## Clone Repository

```bash
git clone https://github.com/AasifMusafir/Construction-Site-Safety-Monitoring-System-.git

cd PPE_Detector
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# YOLO Model Setup

Place the trained model inside:

```text
app/model/
```

Example:

```text
app/model/best.pt
```

---

# Running FastAPI

Start the server from the project root:

```bash
uvicorn app.app:app --reload
```

Expected output:

```text
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

# Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI will appear with all available API endpoints.

---

# Health Check Endpoint

### Request

```http
GET /health
```

### Response

```json
{
  "status": "healthy",
  "model_loaded": true
}
```

---

# PPE Detection Endpoint

### Request

```http
POST /predict
```

Upload an image using:

- Swagger UI
- Postman
- cURL

Form Data:

```text
file=<image>
```

---

## Example Response

```json
{
  "instance_id": "06_23_2026_1",
  "has_person": true,
  "is_compliant": false,
  "missing_ppe": [
    "helmet"
  ],
  "detected_ppe": [
    "hardhat",
    "safety vest"
  ],
  "snapshot": "snapshots/06_23_2026_1_snapshot_1.jpg",
  "inference_time_ms": 120.45,
  "detections": [
    {
      "label": "Person",
      "confidence": 0.95,
      "bbox": [100, 50, 400, 600]
    },
    {
      "label": "NO-Hardhat",
      "confidence": 0.89,
      "bbox": [150, 60, 220, 150]
    }
  ]
}
```

---

# Violation Logging

All compliance results are automatically stored in:

```text
app/logs/violations.csv
```

Example:

```csv
timestamp,instance_id,status,missing_ppe
2026-06-23 10:15:22,06_23_2026_1,NON_COMPLIANT,helmet
```

---

# Snapshot Storage

Violation snapshots are automatically saved to:

```text
app/snapshots/
```

Example:

```text
06_23_2026_1_snapshot_1.jpg
```

Snapshots are only generated for non-compliant detections.

---

# Compliance Logic

Default PPE requirements:

```python
{
    "helmet": True,
    "vest": True,
    "mask": False
}
```

### Compliant Example

Detected:

```text
Person
Hardhat
Safety Vest
```

Result:

```text
COMPLIANT
```

### Non-Compliant Example

Detected:

```text
Person
NO-Hardhat
```

Result:

```text
NON-COMPLIANT
Missing PPE: Helmet
```

---

# Multi-Camera RTSP Monitoring

The system supports multiple RTSP camera streams.

Example:

```python
manager.add_camera(
    "Gate_1",
    "rtsp://admin:password@192.168.1.101:554/stream"
)

manager.add_camera(
    "Gate_2",
    "rtsp://admin:password@192.168.1.102:554/stream"
)
```

Start monitoring:

```python
manager.start_all()
```

Stop monitoring:

```python
manager.stop_all()
```

---

# Deployment Formats

The trained PPE detection model has been exported into multiple deployment formats to support a wide range of inference environments.

| Format | File Extension | Target Platform |
|----------|---------------|----------------|
| PyTorch | .pt | Training and standard inference |
| ONNX | .onnx | Cross-platform deployment |
| TensorRT | .engine | NVIDIA GPUs and Jetson devices |
| TensorFlow Lite | .tflite | Edge devices, Raspberry Pi, Android |

This enables the system to be deployed across cloud, edge, and embedded environments with minimal changes to the application code.

---

# Edge Deployment Support

The PPE Compliance Monitoring System is designed for deployment at the edge, enabling low-latency inference directly on industrial devices without requiring cloud connectivity.

Supported Edge Platforms:

- NVIDIA Jetson Nano
- NVIDIA Jetson Xavier NX
- NVIDIA Jetson Orin
- Raspberry Pi 4/5
- Industrial Edge PCs
- Android-based Edge Devices

Supported Inference Engines:

- PyTorch
- ONNX Runtime
- TensorRT
- TensorFlow Lite

Benefits:

- Reduced latency
- Lower bandwidth requirements
- Improved privacy and security
- Real-time PPE compliance monitoring
- Suitable for remote construction and industrial sites

- ---

# Running Unit Tests

Install pytest:

```bash
pip install pytest
```

Run all tests:

```bash
pytest
```

Run a specific test:

```bash
pytest tests/test_detector.py
```

Expected:

```text
=========================
7 passed
=========================
```

---

# Future Improvements

- DeepSORT/ByteTrack integration for worker tracking
- PostgreSQL integration
- Email/SMS alerts
- Web dashboard
- Restricted zone monitoring
- Analytics and reporting
- GPU Docker deployment
- Light tower/PLC integration

---

# Troubleshooting

## FastAPI Not Starting

Run:

```bash
uvicorn app.app:app --reload
```

Ensure `app.py` contains:

```python
app = FastAPI()
```

---

## Model Not Loading

Verify:

```text
app/model/best.pt
```

exists and is accessible.

---

## Swagger UI Not Opening

Ensure FastAPI is running and open:

```text
http://127.0.0.1:8000/docs
```

---

## Module Import Error

Make sure:

```text
app/
│
├── __init__.py
```

exists.

---

# Tech Stack

- Python
- YOLO
- OpenCV
- FastAPI
- Uvicorn
- Docker
- TensorRT
- TensorFlow Lite
- ONNX Runtime
- RTSP Streaming
- Pandas
- Computer Vision
- Edge AI

---
