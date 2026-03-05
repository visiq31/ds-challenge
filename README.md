# Delivery Prediction and Analytics

This repository contains a full-cycle data science project focused on the Olist marketplace dataset. The objective was to extract meaningful business insights from historical orders and build a robust baseline model to predict delivery delays, aimed at improving customer satisfaction.

## 1. Executive Summary

The project is divided into two main parts: a descriptive analysis of the marketplace's health and a machine learning pipeline for logistical forecasting.

### Key Analytics Findings
After analyzing ~99k orders from 2016 to 2018, three main patterns emerged:
* **Retention Gap:** The repeat purchase rate is remarkably low at 3.06%. Olist currently operates as a high-acquisition, low-retention platform, where most customers do not return for a second purchase within the analyzed timeframe.
* **Satisfaction Detractors:** There is a clear correlation between logistical performance and customer reviews. While the majority of reviews are positive, the spike in 1-star ratings is heavily linked to orders delivered after the estimated date.
* **Revenue vs. Volume:** Certain categories, such as Watches and Health & Beauty, drive the highest Gross Merchandise Value (GMV), despite not having the highest order volume. This suggests a need for segmented logistical strategies based on item value.

## 2. Modeling Strategy

The modeling task was to predict whether an order would be delivered on time (`is_on_time`) based only on information available at the time of purchase.

### Data Split and Evaluation
We implemented a **Temporal Split**, using the first 80% of orders for training and the remaining 20% for testing. This approach is essential for time-dependent data to avoid data leakage and simulate a real production environment.

Due to the class imbalance (only ~5% of orders in the test set were late), we prioritized **PR-AUC (Precision-Recall AUC)** and **ROC-AUC** over accuracy. While accuracy was high for all models, it was a misleading metric that failed to capture operational failures.

### Model Performance
We compared a Random Forest baseline against a tuned LightGBM model using **TimeSeriesSplit** cross-validation.

* **Random Forest:** Achieved an ROC-AUC of 0.51, failing to learn from the imbalanced classes and essentially guessing the majority class.
* **LightGBM:** Achieved an **ROC-AUC of 0.66** and a **PR-AUC of 0.09**. While the precision is low, the model successfully identified 161 actual late deliveries that the baseline missed, providing a clear opportunity for proactive customer communication.

## 3. Project Structure

The project is organized into a modular Python package to ensure maintainability and ease of deployment.

* `artifacts/`: Stores the serialized LightGBM model (`.pkl`).
* `notebooks/`: Contains the exploratory data analysis and model development process.
* `reports/`: Documentation and figures regarding the business analysis.
* `src/`: Core logic including data loading, feature engineering, and inference.
* `tests/`: Unit tests for the feature engineering pipeline.
* `requirements.txt`: Project dependencies.

## 4. Installation and Usage

### Setup
Ensure you have Python 3.9+ installed. Create a virtual environment and install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
```

### Running Tests
To verify the feature engineering logic and data integrity:
```bash
pytest
```

### Inference via CLI
The project provides a command-line interface to predict the delivery status of a specific customer's latest order:
```bash
python -m src.main --customer_id <CUSTOMER_HASH_ID>
```

## 5. Limitations and Future Work

The current model is a baseline and faces a few constraints:
* **Static Geolocation:** We used state-to-state proxies for distance. Integrating exact coordinates from the geolocation dataset to calculate Haversine distance would likely improve accuracy.
* **Feature Store:** Future iterations should include rolling-window features, such as the seller's average delay rate over the last 30 days, to capture recent logistical bottlenecks.

