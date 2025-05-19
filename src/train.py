import os
import shutil
import pandas as pd
import numpy as np
import time
from concrete.ml.sklearn import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from concrete.ml.deployment import FHEModelDev

def train_and_export():
    df = pd.read_csv("data/bio_age_demo_data.csv")
    X = df.drop('Age', axis=1).values
    y = df['Age'].values
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    model = LinearRegression(n_bits=8)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    print(f"MAE: {mean_absolute_error(y_test, y_pred):.2f}")
    print(f"R²: {r2_score(y_test, y_pred):.2f}")
    
    print("\n🛠 Compiling model for FHE...")
    model.compile(X_train)

    # Handle existing artifact directory
    artifact_dir = "fhe_artifacts"
    if os.path.exists(artifact_dir):
        print(f"[INFO] '{artifact_dir}' already exists. Deleting it to avoid conflicts...")
        shutil.rmtree(artifact_dir)


    FHEModelDev("fhe_artifacts", model).save()
    print("FHE model exported to fhe_artifacts/")

    print("\n⏱ Benchmarking Inference Times...")

    # Cleartext inference
    start = time.time()
    y_clear = model.predict(X_test[:1])
    clear_time = time.time() - start

    # FHE inference
    start = time.time()
    y_fhe = model.predict(X_test[:1], fhe="execute")
    fhe_time = time.time() - start

    print("\n[INFO] Inference Times:")
    print(f" - Cleartext: {clear_time * 1000:.2f} ms")
    print(f" - FHE: {fhe_time:.2f} s")
    print(f"MAE Difference (sample): {abs(y_clear[0] - y_fhe[0]):.2f} years")

if __name__ == "__main__":
    train_and_export()
