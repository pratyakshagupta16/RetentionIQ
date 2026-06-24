import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report, confusion_matrix
import os
import pickle

def prepare_churn_dataset(df_features):




    df = df_features.copy()


    y = df["Churned"]


    cols_to_drop = [
        "Customer ID", "Churned", "Recency", "Last Purchase Date",
        "First Purchase Date", "City", "State"
    ]


    X = df.drop(columns=[col for col in cols_to_drop if col in df.columns])


    numeric_cols = X.select_dtypes(include=["int64", "float64", "float32", "int32"]).columns
    categorical_cols = X.select_dtypes(include=["object", "category"]).columns


    for col in numeric_cols:
        X[col] = X[col].fillna(X[col].median() if not X[col].empty else 0)


    for col in categorical_cols:
        if not X[col].empty:
            mode_val = X[col].mode()
            mode_impute = mode_val.iloc[0] if not mode_val.empty else "Unknown"
            X[col] = X[col].fillna(mode_impute)
        else:
            X[col] = X[col].fillna("Unknown")


    if len(categorical_cols) > 0:
        X_encoded = pd.get_dummies(X, columns=categorical_cols, drop_first=True)
    else:
        X_encoded = X.copy()


    X_encoded = X_encoded.select_dtypes(include=[np.number, "bool"]).astype(float)


    feature_names = list(X_encoded.columns)

    return X_encoded, y, feature_names

def train_and_compare_models(df_features, X, y):





    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)


    X_train_scaled_df = pd.DataFrame(X_train_scaled, columns=X_train.columns)
    X_test_scaled_df = pd.DataFrame(X_test_scaled, columns=X_test.columns)


    models = {
        "Logistic Regression": LogisticRegression(random_state=42, max_iter=1000),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "XGBoost": XGBClassifier(random_seed=42, eval_metric="logloss", use_label_encoder=False)
    }

    results = {}
    trained_models = {}

    for name, model in models.items():

        model.fit(X_train_scaled_df, y_train)


        y_pred = model.predict(X_test_scaled_df)
        y_prob = model.predict_proba(X_test_scaled_df)[:, 1]


        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        auc = roc_auc_score(y_test, y_prob)

        results[name] = {
            "Accuracy": acc,
            "Precision": prec,
            "Recall": rec,
            "F1-Score": f1,
            "ROC-AUC": auc
        }

        trained_models[name] = model


    best_name = max(results, key=lambda k: results[k]["F1-Score"])
    best_model = trained_models[best_name]


    best_pred = best_model.predict(X_test_scaled_df)
    best_prob = best_model.predict_proba(X_test_scaled_df)[:, 1]

    accuracy = float(accuracy_score(y_test, best_pred))
    cls_report = classification_report(y_test, best_pred, output_dict=True, zero_division=0)
    conf_matrix = confusion_matrix(y_test, best_pred).tolist()


    X_scaled_all = scaler.transform(X)
    probs_all = best_model.predict_proba(X_scaled_all)[:, 1]
    preds_all = best_model.predict(X_scaled_all)


    predictions_df = pd.DataFrame({
        "Customer ID": df_features["Customer ID"],
        "Churn_Probability": probs_all,
        "Predicted_Churn": np.where(preds_all == 1, "Yes", "No")
    })


    def get_risk_tier(prob):
        if prob <= 0.30:
            return "Low Risk"
        elif prob <= 0.70:
            return "Medium Risk"
        else:
            return "High Risk"

    predictions_df["Churn_Risk"] = predictions_df["Churn_Probability"].apply(get_risk_tier)


    feature_importance_df = get_feature_importance(best_model, list(X.columns))

    return {
        "best_model": best_model,
        "best_model_name": best_name,
        "accuracy": accuracy,
        "predictions": predictions_df,
        "feature_importance": feature_importance_df,
        "classification_report": cls_report,
        "confusion_matrix": conf_matrix,
        "scaler": scaler,
        "feature_names": list(X.columns),
        "metrics": results,
        "X_train": X_train,
        "y_train": y_train
    }

def get_feature_importance(model, feature_names):



    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    elif hasattr(model, "coef_"):
        importances = np.abs(model.coef_[0])
        importances = importances / np.sum(importances)
    else:
        importances = np.ones(len(feature_names)) / len(feature_names)

    df_imp = pd.DataFrame({
        "Feature": feature_names,
        "Importance": importances
    }).sort_values(by="Importance", ascending=False).reset_index(drop=True)

    return df_imp

