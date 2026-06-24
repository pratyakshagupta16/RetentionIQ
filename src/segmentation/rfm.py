import pandas as pd
import numpy as np

def perform_rfm_segmentation(df_rfm):








    df = df_rfm.copy()



    df["R_Score"] = pd.qcut(df["Recency"].rank(method="first"), 5, labels=[5, 4, 3, 2, 1]).astype(int)

    df["F_Score"] = pd.qcut(df["Frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)

    df["M_Score"] = pd.qcut(df["Monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)

    def assign_segment(row):
        r = row["R_Score"]
        f = row["F_Score"]
        m = row["M_Score"]


        if r >= 4 and f >= 4 and m >= 4:
            return "Champions"

        elif r <= 2 and f <= 2 and m <= 2:
            return "Lost Customers"

        elif r <= 2 and (f >= 3 or m >= 3):
            return "At Risk"

        elif f >= 3 and m >= 3:
            return "Loyal Customers"

        else:
            return "Potential Loyalists"

    df["Segment"] = df.apply(assign_segment, axis=1)


    unique_segments = list(df["Segment"].unique())
    label_mapping = {seg: seg for seg in unique_segments}


    df = df.drop(columns=["R_Score", "F_Score", "M_Score"])

    return df, label_mapping
