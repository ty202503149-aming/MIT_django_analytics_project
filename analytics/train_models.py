import os
import sys
import django
import joblib
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, LogisticRegression

# Add project root (where manage.py lives) to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Point to Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from analytics.models import StudentRecord


def load_data():
    qs = StudentRecord.objects.all().values(
        "age",
        "gender",
        "gaming_hours",
        "study_hours",
        "sleep_hours",
        "attendance",
        "gaming_genre",
        "social_activity",
        "device_usage",
        "reaction_time_ms",
        "addiction_score",
        "stress_level",
        "grades",
    )
    data = list(qs)

    import pandas as pd
    df = pd.DataFrame(data)
    return df


def train_models():
    df = load_data()

    feature_cols = [
        "age",
        "gender",
        "gaming_hours",
        "study_hours",
        "sleep_hours",
        "attendance",
        "gaming_genre",
        "social_activity",
        "device_usage",
        "reaction_time_ms",
    ]

    X = df[feature_cols]
    y_addiction = df["addiction_score"]
    y_stress = df["stress_level"]

    cat_cols = ["gender", "gaming_genre"]
    num_cols = [c for c in feature_cols if c not in cat_cols]

    # Numeric features scaled, categorical features one-hot encoded
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ]
    )

    addiction_model = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("model", LinearRegression()),
        ]
    )

    stress_model = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("model", LogisticRegression(max_iter=2000)),  # increased max_iter
        ]
    )

    X_train, X_test, y_add_train, y_add_test = train_test_split(
        X, y_addiction, test_size=0.2, random_state=42
    )
    X_train_s, X_test_s, y_str_train, y_str_test = train_test_split(
        X, y_stress, test_size=0.2, random_state=42
    )

    addiction_model.fit(X_train, y_add_train)
    stress_model.fit(X_train_s, y_str_train)

    os.makedirs("ml", exist_ok=True)
    joblib.dump(addiction_model, os.path.join("ml", "addiction_model.joblib"))
    joblib.dump(stress_model, os.path.join("ml", "stress_model.joblib"))


if __name__ == "__main__":
    train_models()
    print("Models trained and saved.")