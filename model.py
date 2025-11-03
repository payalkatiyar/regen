"""train_model_compare.py

This script trains several regression models and saves the best one.

Changes made:
- Try to load `data.csv` first, then fall back to `dataset.csv`.
- Use logging instead of raw prints.
- Wrap execution in a `main()` and protect with
  `if __name__ == "__main__":` so importing from `app.py`
  won't run a long training job silently.
"""

import os
import logging
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
import xgboost as xgb
import pickle

logging.basicConfig(level=logging.INFO, format="%(message)s")


def load_data():
    # try common filenames so the script works with either `data.csv` or `dataset.csv`
    candidates = ["data.csv", "dataset.csv"]
    cwd = os.getcwd()
    for fn in candidates:
        path = os.path.join(cwd, fn)
        if os.path.exists(path):
            logging.info(f"Loading data from {path}")
            return pd.read_csv(path)
    raise FileNotFoundError(
        f"None of the candidates {candidates} were found in {cwd}."
    )


def train_and_save(data):
    # -------------------- Features & Target --------------------
    if "generated_power_kw" not in data.columns:
        raise KeyError("Target column 'generated_power_kw' not found in the data")

    X = data.drop(columns=["generated_power_kw"])
    y = data["generated_power_kw"]

    # -------------------- Split Data --------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # -------------------- Define Models --------------------
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=200, random_state=42),
        "Gradient Boosting": GradientBoostingRegressor(n_estimators=200, random_state=42),
        "XGBoost": xgb.XGBRegressor(
            n_estimators=300, learning_rate=0.05, max_depth=6, subsample=0.8, random_state=42
        ),
        "Support Vector Regressor": SVR(kernel="rbf", C=100, gamma=0.1, epsilon=0.1)
    }

    # -------------------- Train and Evaluate --------------------
    results = []

    for name, model in models.items():
        logging.info(f"\n🔹 Training {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        results.append((name, r2, mae))
        logging.info(f"R² Score: {r2:.4f} | MAE: {mae:.4f}")

    # -------------------- Compare Results --------------------
    results_df = pd.DataFrame(results, columns=["Model", "R2_Score", "MAE"])
    results_df = results_df.sort_values(by="R2_Score", ascending=False)
    logging.info("\n🏁 Model Comparison Results:")
    logging.info("\n" + results_df.to_string(index=False))

    # -------------------- Save Best Model --------------------
    best_model_name = results_df.iloc[0, 0]
    best_r2 = results_df.iloc[0, 1]
    best_model = models[best_model_name]

    with open("model.pkl", "wb") as f:
        pickle.dump(best_model, f)

    logging.info(f"\n✅ Best Model: {best_model_name}")
    logging.info(f"🏆 R² Score: {best_r2:.4f}")
    logging.info("💾 Saved as model.pkl")


def main():
    try:
        data = load_data()
    except Exception as e:
        logging.error(f"Failed to load data: {e}")
        return

    try:
        train_and_save(data)
    except Exception as e:
        logging.error(f"Training failed: {e}")


if __name__ == "__main__":
    main()

