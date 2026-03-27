# 🔧 Predictive Maintenance System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9-blue?style=for-the-badge&logo=python&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-SageMaker-orange?style=for-the-badge&logo=amazon-aws&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-1.7.6-green?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Live-red?style=for-the-badge&logo=streamlit&logoColor=white)

**An end-to-end machine failure prediction system built on AWS.**  
Real-time inference · Automated email alerts · Live web dashboard

[🚀 Live Demo](#) · [📖 Documentation](#architecture) · [🐛 Report Bug](../../issues)

</div>

---

## 📸 Overview

This project predicts whether an industrial machine is likely to fail based on sensor readings. When a failure is detected, an automated email alert is triggered instantly via Amazon SNS.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Customer Application                  │
│                  (Streamlit Dashboard)                   │
└─────────────────────────┬───────────────────────────────┘
                          │ HTTP POST
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  Amazon API Gateway                      │
│                   REST API (prod)                        │
└─────────────────────────┬───────────────────────────────┘
                          │ triggers
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    AWS Lambda                            │
│              trigger-endpoint function                   │
└──────────────┬──────────────────────┬───────────────────┘
               │                      │
               ▼                      ▼
┌──────────────────────┐   ┌─────────────────────────────┐
│  Amazon SageMaker    │   │        Amazon SNS            │
│  XGBoost Endpoint    │   │    Email Notification        │
│  (ml.m5.large)       │   │  (on failure prediction)     │
└──────────────────────┘   └─────────────────────────────┘
```

---

## ✨ Features

- 🤖 **ML Model** — XGBoost classifier trained on 124,000+ sensor readings
- ⚡ **Real-time inference** — predictions in under 300ms
- 📧 **Automated alerts** — instant email via SNS when failure is detected
- 🌐 **REST API** — publicly accessible via Amazon API Gateway
- 📊 **Live dashboard** — interactive Streamlit web app
- ☁️ **Fully serverless** — Lambda + API Gateway, zero server management

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **ML Model** | XGBoost 1.7.6 |
| **Resampling** | SMOTE (imbalanced-learn) |
| **Model Hosting** | Amazon SageMaker |
| **Model Storage** | Amazon S3 |
| **Serverless** | AWS Lambda |
| **API** | Amazon API Gateway |
| **Alerts** | Amazon SNS |
| **Frontend** | Streamlit |
| **Language** | Python 3.9 |

---

## 📁 Project Structure

```
predictive-maintenance/
│
├── app.py                                    ← Streamlit dashboard
├── inference.py                              ← SageMaker serving script
├── requirements.txt                          ← Python dependencies
├── README.md
│
└── notebooks/
    ├── Predictive_maintainance_model.ipynb   ← Model training
    └── pred_model.ipynb                      ← SageMaker deployment
```

---

## 📊 Dataset

- **Source:** Predictive maintenance sensor dataset
- **Size:** 124,494 records × 12 features
- **Class imbalance:** Only 106 failures (0.085%) — handled with SMOTE

| Feature | Description |
|---|---|
| `device` | Encoded machine ID |
| `metric1` | Sensor reading 1 |
| `metric2` | Sensor reading 2 |
| `metric3` | Sensor reading 3 |
| `metric4` | Sensor reading 4 |
| `metric5` | Sensor reading 5 |
| `metric6` | Sensor reading 6 |
| `metric7` | Sensor reading 7 |
| `metric8` | Sensor reading 8 |
| `metric9` | Sensor reading 9 |
| `failure` | Target (0 = healthy, 1 = failure) |

---

## 🤖 Model Performance

```
Accuracy: 98.26%

              precision    recall  f1-score   support
           0       1.00      0.98      0.99     24881
           1       0.01      0.28      0.02        18

Decision threshold: 0.12 (tuned for higher recall on failure class)
```

> ℹ️ The low precision on the failure class is intentional — in predictive maintenance, missing a real failure is far more costly than a false alarm.

---

## 🚀 Local Setup

**1. Clone the repo**
```bash
git clone https://github.com/your-username/predictive-maintenance.git
cd predictive-maintenance
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
streamlit run app.py
```

---

## 🔌 API Usage

**Endpoint:**
```
POST https://your-api-gateway-url/prod/predict
```

**Request body:**
```json
{
  "input": [[device, metric1, metric2, metric3, metric4, metric5, metric6, metric7, metric8, metric9]]
}
```

**Example (Python):**
```python
import requests

response = requests.post(
    "https://your-api-gateway-url/prod/predict",
    json={"input": [[266, 215630672, 55, 6, 11, 13, 407438, 0, 0, 7]]}
)
print(response.json())
```

**Response:**
```json
{
  "prediction": 0,
  "alert_sent": false
}
```

| Field | Type | Description |
|---|---|---|
| `prediction` | int | 0 = healthy, 1 = failure |
| `alert_sent` | bool | True if SNS email was triggered |

---

## ☁️ AWS Deployment

The model is deployed on Amazon SageMaker using the XGBoost container:

```python
from sagemaker.xgboost.model import XGBoostModel

model = XGBoostModel(
    model_data="s3://your-bucket/model/model.tar.gz",
    role=role,
    entry_point="inference.py",
    framework_version="1.7-1"
)

predictor = model.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large"
)
```

---

## 💰 Cost Management

> ⚠️ Delete the SageMaker endpoint when not in use — it costs ~$0.115/hour

```python
import boto3
sm = boto3.client("sagemaker", region_name="ap-south-1")
sm.delete_endpoint(EndpointName="your-endpoint-name")
```

| Service | Cost when idle |
|---|---|
| SageMaker endpoint | ~$0.115/hour |
| Lambda | Free (pay per call) |
| API Gateway | Free (pay per call) |
| SNS | Free |
| S3 | ~$0.001/month |

---

## 📄 License

This project is for educational purposes.

---

<div align="center">
  Built using AWS SageMaker · Lambda · API Gateway · SNS · Streamlit
</div>
