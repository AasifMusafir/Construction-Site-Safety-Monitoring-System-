from app.detector import InstanceDetector


def test_compliant_person():

    detector = InstanceDetector()

    detections = [
        {"class": "Person"},
        {"class": "Hardhat"},
        {"class": "Safety Vest"}
    ]

    result = detector.process_detection(detections)

    assert result["has_person"] is True
    assert result["is_compliant"] is True


def test_missing_helmet():

    detector = InstanceDetector()

    detections = [
        {"class": "Person"},
        {"class": "Safety Vest"}
    ]

    result = detector.process_detection(detections)

    assert result["has_person"] is True


def test_no_person():

    detector = InstanceDetector()

    detections = [
        {"class": "Hardhat"}
    ]

    result = detector.process_detection(detections)

    assert result["has_person"] is False