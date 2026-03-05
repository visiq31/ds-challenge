import pytest
import pandas as pd
from src.features import prepare_features

def test_feature_engineering_structure():
    """
    Unit Test to verify that feature engineering produces the correct shape
    and handles all expected columns, including the new 'payment_type'.
    """
    # 1. Create Mock Data (simulating a raw row from the database)
    mock_data = pd.DataFrame({
        'order_id': ['123'],
        'order_purchase_timestamp': pd.to_datetime(['2018-01-01']),
        'order_estimated_delivery_date': pd.to_datetime(['2018-01-10']),
        'order_delivered_customer_date': pd.to_datetime(['2018-01-09']),
        'total_price': [100.0], 
        'total_freight': [20.0], 
        'total_items': [1],
        'product_weight_g': [500.0], 
        'customer_state': ['SP'], 
        'seller_state': ['RJ'],
        'product_category_name_english': ['health_beauty'],
        'payment_type': ['credit_card'] # Ensuring our new feature is tested
    })
    
    # 2. Run the function
    X, _, _ = prepare_features(mock_data, is_train=False)
    
    # 3. Assertions (Validation)
    # Check if the payment_type column exists
    assert 'payment_type' in X.columns
    
    # Check if we have exactly the 7 features selected in config.py
    # (estimated_days, price, freight, items, weight, distance_proxy, payment)
    expected_cols = 12 # 5 Numeric + 7 Categorical
    assert X.shape[1] == expected_cols 
    assert X.iloc[0]['is_same_state'] == 0