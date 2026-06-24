import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules

def perform_market_basket_analysis(df_txns, min_support=0.01, min_confidence=0.1, min_lift=1.0):




    try:

        basket = (df_txns.groupby(["Transaction ID", "Product Name"])["Quantity"]
                  .sum()
                  .unstack()
                  .reset_index()
                  .fillna(0)
                  .set_index("Transaction ID"))


        basket_sets = basket.map(lambda x: x > 0)


        basket_sets = basket_sets[basket_sets.sum(axis=1) > 1]

        if basket_sets.empty:
            return pd.DataFrame(columns=["antecedents", "consequents", "support", "confidence", "lift", "leverage"])


        frequent_itemsets = apriori(basket_sets, min_support=min_support, use_colnames=True)

        if frequent_itemsets.empty:
            return pd.DataFrame(columns=["antecedents", "consequents", "support", "confidence", "lift", "leverage"])


        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=min_lift)


        rules = rules[rules["confidence"] >= min_confidence]

        if rules.empty:
            return pd.DataFrame(columns=["antecedents", "consequents", "support", "confidence", "lift", "leverage"])


        rules["antecedents_str"] = rules["antecedents"].apply(lambda x: ", ".join(list(x)))
        rules["consequents_str"] = rules["consequents"].apply(lambda x: ", ".join(list(x)))


        rules = rules.sort_values(by="lift", ascending=False).reset_index(drop=True)

        return rules

    except Exception as e:
        print(f"Error in Market Basket Analysis: {e}")

        return pd.DataFrame(columns=[
            "antecedents_str", "consequents_str", "support",
            "confidence", "lift", "leverage", "antecedents", "consequents"
        ])
