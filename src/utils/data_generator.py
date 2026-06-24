import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_synthetic_data(num_customers=500, num_transactions=4000, random_seed=42):




    np.random.seed(random_seed)


    locations = [
        {"city": "San Francisco", "state": "CA", "lat": 37.7749, "lon": -122.4194},
        {"city": "Los Angeles", "state": "CA", "lat": 34.0522, "lon": -118.2437},
        {"city": "New York", "state": "NY", "lat": 40.7128, "lon": -74.0060},
        {"city": "Austin", "state": "TX", "lat": 30.2672, "lon": -97.7431},
        {"city": "Houston", "state": "TX", "lat": 29.7604, "lon": -95.3698},
        {"city": "Miami", "state": "FL", "lat": 25.7617, "lon": -80.1918},
        {"city": "Orlando", "state": "FL", "lat": 28.5383, "lon": -81.3792},
        {"city": "Chicago", "state": "IL", "lat": 41.8781, "lon": -87.6298},
        {"city": "Seattle", "state": "WA", "lat": 47.6062, "lon": -122.3321},
        {"city": "Boston", "state": "MA", "lat": 42.3601, "lon": -71.0589}
    ]


    products_by_category = {
        "Electronics": [("Laptop", 1200), ("Smartphone", 800), ("Headphones", 150), ("Smartwatch", 250), ("Monitor", 350), ("Keyboard & Mouse", 80)],
        "Apparel": [("Designer Jacket", 180), ("Jeans", 70), ("Sneakers", 110), ("Hoodie", 60), ("Sunglasses", 140), ("Sports T-Shirt", 35)],
        "Home & Kitchen": [("Espresso Machine", 450), ("Air Fryer", 120), ("Blender", 90), ("Robot Vacuum", 300), ("Chef Knife Set", 150), ("Mug Set", 30)],
        "Books": [("SaaS Marketing Playbook", 25), ("Machine Learning Basics", 45), ("Leadership Biography", 30), ("Fantasy Novel", 20), ("Self-Improvement Guide", 18)],
        "Beauty & Health": [("Skincare Serum", 65), ("Dior Perfume", 110), ("Electric Toothbrush", 85), ("Multivitamins", 25), ("Hair Dryer", 95)]
    }


    customer_ids = [f"CUST-{i:04d}" for i in range(1, num_customers + 1)]
    genders = ["Male", "Female", "Non-binary"]
    gender_p = [0.47, 0.49, 0.04]

    customers_data = []


    end_date = datetime(2026, 6, 1)
    start_date = datetime(2024, 6, 1)
    total_days = (end_date - start_date).days

    for cid in customer_ids:


        cust_profile_type = np.random.choice([1, 2, 3, 4], p=[0.15, 0.40, 0.30, 0.15])


        loc = np.random.choice(locations)

        age = int(np.clip(np.random.normal(loc=38, scale=12), 18, 75))
        gender = np.random.choice(genders, p=gender_p)


        if cust_profile_type == 1:
            web_visits = np.random.randint(45, 120)
            email_opens = np.random.randint(30, 90)
            satisfaction = np.random.choice([4, 5], p=[0.3, 0.7])
            tenure_days = np.random.randint(300, total_days)
        elif cust_profile_type == 2:
            web_visits = np.random.randint(25, 80)
            email_opens = np.random.randint(15, 60)
            satisfaction = np.random.choice([3, 4, 5], p=[0.1, 0.6, 0.3])
            tenure_days = np.random.randint(150, total_days)
        elif cust_profile_type == 3:
            web_visits = np.random.randint(5, 35)
            email_opens = np.random.randint(2, 20)
            satisfaction = np.random.choice([2, 3, 4], p=[0.15, 0.60, 0.25])
            tenure_days = np.random.randint(30, 400)
        else:
            web_visits = np.random.randint(1, 15)
            email_opens = np.random.randint(0, 5)
            satisfaction = np.random.choice([1, 2, 3], p=[0.4, 0.4, 0.2])
            tenure_days = np.random.randint(30, 250)

        customers_data.append({
            "Customer ID": cid,
            "Age": age,
            "Gender": gender,
            "City": loc["city"],
            "State": loc["state"],
            "Latitude": loc["lat"],
            "Longitude": loc["lon"],
            "Website Visits": web_visits,
            "Email Opens": email_opens,
            "Customer Satisfaction Score": satisfaction,
            "_profile_type": cust_profile_type,
            "_tenure_days": tenure_days
        })

    df_customers = pd.DataFrame(customers_data)


    transactions_data = []
    txn_id_counter = 10001



    pairs = [
        ("Laptop", "Keyboard & Mouse", "Electronics"),
        ("Espresso Machine", "Mug Set", "Home & Kitchen"),
        ("Skincare Serum", "Dior Perfume", "Beauty & Health"),
        ("Designer Jacket", "Sunglasses", "Apparel")
    ]

    for i in range(num_transactions):

        cust_idx = np.random.randint(0, num_customers)
        cust = df_customers.iloc[cust_idx]
        cid = cust["Customer ID"]
        profile_type = cust["_profile_type"]
        tenure_days = cust["_tenure_days"]



        if profile_type == 4:
            max_offset = total_days - 100
            min_offset = max(0, max_offset - tenure_days)
            if min_offset >= max_offset:
                min_offset = 0
            txn_day_offset = np.random.randint(min_offset, max_offset + 1)
        else:
            min_offset = max(0, total_days - tenure_days)
            txn_day_offset = np.random.randint(min_offset, total_days)

        txn_date = start_date + timedelta(days=int(txn_day_offset))


        category = np.random.choice(list(products_by_category.keys()), p=[0.3, 0.2, 0.2, 0.15, 0.15])


        prod_list = products_by_category[category]
        prod_idx = np.random.randint(0, len(prod_list))
        product_name, base_price = prod_list[prod_idx]



        if profile_type == 1:
            quantity = np.random.choice([1, 2, 3, 4], p=[0.4, 0.3, 0.2, 0.1])
            price_mult = np.random.uniform(0.95, 1.15)
        elif profile_type == 2:
            quantity = np.random.choice([1, 2, 3], p=[0.6, 0.3, 0.1])
            price_mult = np.random.uniform(0.90, 1.05)
        else:
            quantity = np.random.choice([1, 2], p=[0.85, 0.15])
            price_mult = np.random.uniform(0.85, 1.00)

        purchase_amt = round(base_price * price_mult * quantity, 2)

        transactions_data.append({
            "Transaction ID": f"TXN-{txn_id_counter}",
            "Customer ID": cid,
            "Purchase Date": txn_date.strftime("%Y-%m-%d"),
            "Product Name": product_name,
            "Product Category": category,
            "Quantity": quantity,
            "Purchase Amount": purchase_amt
        })

        txn_id_counter += 1


        if np.random.rand() < 0.25:

            for item1, item2, pair_cat in pairs:
                if product_name == item1:

                    pair_prod_list = products_by_category[pair_cat]
                    item2_price = [item[1] for item in pair_prod_list if item[0] == item2][0]
                    transactions_data.append({
                        "Transaction ID": f"TXN-{txn_id_counter}",
                        "Customer ID": cid,
                        "Purchase Date": txn_date.strftime("%Y-%m-%d"),
                        "Product Name": item2,
                        "Product Category": pair_cat,
                        "Quantity": 1,
                        "Purchase Amount": round(item2_price * np.random.uniform(0.9, 1.1), 2)
                    })
                    txn_id_counter += 1
                    break

    df_txns = pd.DataFrame(transactions_data)


    df_combined = pd.merge(df_txns, df_customers, on="Customer ID", how="inner")


    cols_to_keep = [col for col in df_combined.columns if not col.startswith("_")]
    df_final = df_combined[cols_to_keep].sort_values(by=["Purchase Date", "Transaction ID"]).reset_index(drop=True)

    return df_final

def ensure_sample_data_exists(filepath="data/raw/sample_customer_data.csv"):



    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if not os.path.exists(filepath):
        df = generate_synthetic_data()
        df.to_csv(filepath, index=False)
        print(f"Generated sample synthetic data at: {filepath}")
    return filepath

if __name__ == "__main__":
    ensure_sample_data_exists()
