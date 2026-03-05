import pandas as pd
from src.config import NUMERIC_FEATURES, CATEGORICAL_FEATURES, TARGET_COL

def prepare_features(df: pd.DataFrame, is_train: bool = True):
    """Feature engineering logic matching training steps."""
    df = df.copy()

    if is_train:
        df = df.dropna(subset=['order_delivered_customer_date', 'order_estimated_delivery_date'])
        df[TARGET_COL] = (df['order_delivered_customer_date'] <= df['order_estimated_delivery_date']).astype(int)

    # Engineering
    df['estimated_delivery_days'] = (df['order_estimated_delivery_date'] - df['order_purchase_timestamp']).dt.days
    df['purchase_month'] = df['order_purchase_timestamp'].dt.month
    df['purchase_day_of_week'] = df['order_purchase_timestamp'].dt.dayofweek
    df['is_same_state'] = (df['customer_state'] == df['seller_state']).astype(int)

    # Filling NAs (Strategies defined in Notebook analysis)
    df['product_category_name_english'] = df['product_category_name_english'].fillna('unknown')
    df['payment_type'] = df['payment_type'].fillna('unknown')
    df['product_weight_g'] = df['product_weight_g'].fillna(650.0) 
    df['total_items'] = df['total_items'].fillna(1)
    df['total_price'] = df['total_price'].fillna(0)
    df['total_freight'] = df['total_freight'].fillna(0)
    df['estimated_delivery_days'] = df['estimated_delivery_days'].fillna(20)

    # Selection
    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    
    if is_train:
        y = df[TARGET_COL]
        return X, y, df
    
    return X, None, df