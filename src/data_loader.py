import os
import pandas as pd
from src.config import DATA_DIR

def load_raw_data():
    """Loads all necessary datasets from the DATA_DIR."""
    try:
        datasets = {
            'orders': pd.read_csv(os.path.join(DATA_DIR, "olist_orders_dataset.csv"),
                                parse_dates=['order_purchase_timestamp', 'order_estimated_delivery_date', 
                                             'order_delivered_customer_date']),
            'items': pd.read_csv(os.path.join(DATA_DIR, "olist_order_items_dataset.csv")),
            'customers': pd.read_csv(os.path.join(DATA_DIR, "olist_customers_dataset.csv")),
            'products': pd.read_csv(os.path.join(DATA_DIR, "olist_products_dataset.csv")),
            'sellers': pd.read_csv(os.path.join(DATA_DIR, "olist_sellers_dataset.csv")),
            'translation': pd.read_csv(os.path.join(DATA_DIR, "product_category_name_translation.csv")),
            'payments': pd.read_csv(os.path.join(DATA_DIR, "olist_order_payments_dataset.csv"))
        }
        return datasets
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Could not find datasets in {DATA_DIR}. Check your path.") from e

def build_abt(datasets):
    """Constructs the ABT merging all datasets (Inference Logic)."""
    orders = datasets['orders']
    items = datasets['items']
    customers = datasets['customers']
    sellers = datasets['sellers']
    products = datasets['products']
    trans = datasets['translation']
    payments = datasets['payments']

    df = orders.copy()
    
    # Aggregations
    items_agg = items.groupby('order_id').agg(
        total_price=('price', 'sum'),
        total_freight=('freight_value', 'sum'),
        total_items=('order_item_id', 'count'),
        seller_id=('seller_id', 'first'),
        product_id=('product_id', 'first')
    ).reset_index()

    # Payment Aggregation (First payment type per order)
    pay_agg = payments.groupby('order_id')['payment_type'].first().reset_index()

    # Merges
    df = df.merge(items_agg, on='order_id', how='left')
    df = df.merge(customers[['customer_id', 'customer_unique_id', 'customer_state']], on='customer_id', how='left')
    df = df.merge(sellers[['seller_id', 'seller_state']], on='seller_id', how='left')
    df = df.merge(pay_agg, on='order_id', how='left')
    
    products = products.merge(trans, on='product_category_name', how='left')
    df = df.merge(products[['product_id', 'product_category_name_english', 'product_weight_g']], on='product_id', how='left')

    return df