import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")

# Output Paths
MODEL_PATH = os.path.join(ARTIFACTS_DIR, "on_time_delivery_model.pkl")

# Feature Lists (Must match EXACTLY what was used in training)
NUMERIC_FEATURES = [
    'estimated_delivery_days', 'total_price', 'total_freight', 
    'total_items', 'product_weight_g'
]
CATEGORICAL_FEATURES = [
    'purchase_month', 'purchase_day_of_week', 'is_same_state', 
    'customer_state', 'seller_state', 'product_category_name_english',
    'payment_type'
]
TARGET_COL = 'is_on_time'