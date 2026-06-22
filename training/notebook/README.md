# Dataset Research and Selection

## Objective

The objective of this project is to develop a real-time Personal Protective Equipment (PPE) Compliance Monitoring System capable of detecting workers and identifying whether they are wearing the required safety equipment such as hardhats, safety vests, and masks.

To ensure robust model performance, multiple publicly available datasets were researched and evaluated before selecting the final dataset.

---

## Dataset Options Evaluated

### 1. Construction Site Safety Image Dataset (Roboflow)

**Dataset Link:**  
https://www.kaggle.com/datasets/snehilsanyal/construction-site-safety-image-dataset-roboflow

**Classes:**

- Hardhat
- Mask
- NO-Hardhat
- NO-Mask
- NO-Safety Vest
- Person
- Safety Cone
- Safety Vest
- Machinery
- Vehicle

#### Advantages

- PPE-specific annotations.
- Includes both compliant and non-compliant classes.
- Available in YOLO annotation format.
- Contains realistic construction-site scenarios.
- Suitable for industrial safety monitoring applications.

#### Limitations

- Moderate dataset size.
- Some class imbalance between PPE and non-PPE categories.

---

### 2. Hard Hat Detection Dataset

**Dataset Link:**  
https://www.kaggle.com/datasets/andrewmvd/hard-hat-detection

**Classes:**

- Helmet
- Person
- Head

#### Advantages

- High-quality annotations.
- Large number of training images.
- Widely used benchmark dataset.

#### Limitations

- Focuses only on helmet detection.
- Does not contain safety vest or mask annotations.
- Cannot be directly used for complete PPE compliance monitoring.

---

### 3. Construction Safety Dataset

**Dataset Link:**  
https://universe.roboflow.com/test-levac/construction-site-safety-jejzr

**Classes:**

- Person
- Hardhat
- Safety Vest
- Mask
- NO-Hardhat
- NO-Mask
- NO-Safety Vest
- Gloves

#### Advantages

- PPE-focused dataset.
- Includes PPE violation classes.
- Construction-site imagery.

#### Limitations

- Smaller dataset size.
- Limited environmental diversity.

---

### 4. Construction Safety GSNVB Dataset

**Dataset Link:**  
https://huggingface.co/datasets/LibreYOLO/construction-safety-gsnvb

**Classes:**

- Helmet
- No-Helmet
- Vest
- No-Vest
- Person

#### Advantages

- Designed specifically for PPE compliance tasks.
- Contains positive and negative PPE classes.
- Suitable for object detection benchmarking.

#### Limitations

- Limited PPE categories.
- Fewer contextual objects compared to larger datasets.

---

## Dataset Comparison

| Dataset | PPE Classes | Violation Classes | Construction Environment | YOLO Format |
|----------|------------|------------------|--------------------------|------------|
| Construction Site Safety Image Dataset | ✅ | ✅ | ✅ | ✅ |
| Hard Hat Detection Dataset | ❌ | ❌ | ✅ | ❌ |
| Construction Safety Dataset | ✅ | ✅ | ✅ | ✅ |
| Construction Safety GSNVB Dataset | ✅ | ✅ | ✅ | ✅ |

---

## Final Dataset Selection

### Selected Dataset

**Construction Site Safety Image Dataset (Roboflow)**

Dataset Link:  
https://www.kaggle.com/datasets/snehilsanyal/construction-site-safety-image-dataset-roboflow

---

## Justification for Selection

The Construction Site Safety Image Dataset was selected for this project because it best aligns with the project requirements and industrial use case.

Key reasons for selection include:

1. Provides both PPE-compliant and PPE-violation classes.
2. Contains all major PPE categories required for compliance monitoring:
   - Hardhat
   - Safety Vest
   - Mask
3. Includes violation classes:
   - NO-Hardhat
   - NO-Safety Vest
   - NO-Mask
4. Available directly in YOLO annotation format, simplifying training and deployment.
5. Includes contextual construction-site objects such as machinery and vehicles.
6. Closely represents real-world workplace safety scenarios.
7. Suitable for deployment in real-time PPE monitoring systems using YOLO, TensorRT, ONNX, and TensorFlow Lite.

---

## Dataset Statistics

| Attribute | Value |
|------------|--------|
| Number of Classes | 10 |
| Annotation Format | YOLO |
| Training Split | Available |
| Validation Split | Available |
| Test Split | Available |
| PPE Classes | Hardhat, Safety Vest, Mask |
| Violation Classes | NO-Hardhat, NO-Safety Vest, NO-Mask |

---

## Conclusion

After evaluating multiple publicly available PPE datasets, the Construction Site Safety Image Dataset was selected as the primary training dataset due to its comprehensive PPE annotations, inclusion of violation classes, YOLO compatibility, and strong alignment with real-world industrial safety monitoring requirements. The dataset provides an effective foundation for building a robust PPE Compliance Monitoring System capable of detecting both compliant and non-compliant workers in construction environments.
