# 🔧 Predictive Maintenance System

A machine failure prediction system built on AWS using XGBoost and real-time inference.

## Architecture

```
Customer App (Streamlit)
        ↓
Amazon API Gateway
        ↓
AWS Lambda (trigger-endpoint)
        ↓                    ↓
Amazon SageMaker         Amazon SNS
  (XGBoost Model)      (Email Alert)
```

## Features

- Real-time machine failure prediction using XGBoost
- Automated email alerts via Amazon SNS when failure is detected
- REST API via Amazon API Gateway
- Interactive Streamlit dashboard

## Tech Stack

| Layer | Service |
|---|---|
| ML Model | XGBoost (trained locally, deployed on SageMaker) |
| Inference | Amazon SageMaker Endpoint |
| Serverless | AWS Lambda |
| API | Amazon API Gateway |
| Alerts | Amazon SNS (Email) |
| Frontend | Streamlit |

## Dataset

The model is trained on a predictive maintenance dataset with the following features:

| Feature | Description |
|---|---|
| device | Encoded device ID |
| metric1 - metric9 | Sensor readings from the machine |
| failure | Target variable (0 = healthy, 1 = failure) |

The dataset is highly imbalanced (106 failures out of 124,494 records). SMOTE oversampling was used during training to handle this.

## Model

- Algorithm: XGBoost Classifier
- Resampling: SMOTE
- Decision threshold: 0.12 (tuned for higher recall on failure class)
- Accuracy: ~98%

## Local Setup

```bash
# Clone the repo
git clone https://github.com/your-username/predictive-maintenance.git
cd predictive-maintenance

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## API Usage

**Endpoint:**
```
https://your-api-gateway-url/prod/predict

```

**Request:**
```json
{
  "input": [[266, 215630672, 55, 6, 11, 13, 407438, 0, 0, 7]]
}
```

**Response:**
```json
{
  "prediction": 0,
  "alert_sent": false
}
```

## Project Structure

```
predictive-maintenance/
│
├── app.py                              ← Streamlit dashboard
├── requirements.txt                    ← Python dependencies
├── README.md                           ← Project documentation
├── inference.py                        ← SageMaker serving script
│
└── notebooks/
    ├── Predictive_maintainance_model.ipynb   ← Model training
    └── pred_model.ipynb                      ← SageMaker deployment
```
