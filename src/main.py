import argparse
import logging
import pandas as pd
from src.data_loader import load_raw_data, build_abt
from src.features import prepare_features
from src.model import load_model, predict_on_time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def run_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--customer_id", type=str, help="Customer ID for inference")
    parser.add_argument("--top_k", type=int, default=5, help="Ignored (Compatibility arg)")
    args = parser.parse_args()

    if args.customer_id:
        logger.info(f"Starting Inference for Customer: {args.customer_id}")
        
        # 1. Load & Build ABT
        datasets = load_raw_data()
        df_abt = build_abt(datasets)
        
        # 2. Find Customer Order
        customer_orders = df_abt[df_abt['customer_id'] == args.customer_id]
        if customer_orders.empty:
            logger.error(f"Customer {args.customer_id} not found in dataset.")
            return

        # 3. Get Latest Order
        latest_order = customer_orders.sort_values('order_purchase_timestamp', ascending=False).head(1)
        order_id = latest_order['order_id'].values[0]
        
        # 4. Feature Prep
        X_input, _, _ = prepare_features(latest_order, is_train=False)

        try:
            # 5. Predict
            model = load_model()
            probs = predict_on_time(model, X_input)
            prob_late = probs[0][0] # Class 0 is Late
            
            # Using 0.5 threshold as baseline, though business could tune this
            status = "LATE" if prob_late > 0.5 else "ON TIME"
            
            print("\n" + "="*50)
            print(f"PREDICTION FOR ORDER: {order_id}")
            print("="*50)
            print(f"Risk of Delay:   {prob_late:.2%}")
            print(f"Predicted Status: {status}")
            print("="*50 + "\n")
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")

if __name__ == "__main__":
    run_cli()