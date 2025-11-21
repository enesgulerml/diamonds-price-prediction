import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor
import numpy as np

from src.config import (
    PROCESSED_DATA_PATH,
    MLFLOW_TRACKING_URI,
    MLFLOW_EXPERIMENT_NAME,
    MODEL_REGISTRY_NAME,
    RANDOM_STATE,
    PARAM_GRID,
    CV_FOLDS,
    SCORING_METRIC
)
from src.data_processing import get_train_test_split

def eval_metrics(actual, pred):
    """Calculates regression metrics"""
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2

def train_model():
    print("Training model...")

    X_train, X_test, y_train, y_test = get_train_test_split()

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

    print(f"MLflow Server: {MLFLOW_TRACKING_URI}")
    print(f"Experiment Name: {MLFLOW_EXPERIMENT_NAME}")

    with mlflow.start_run(run_name="XGBoost_v1_Base"):


        xgb = XGBRegressor(random_state=RANDOM_STATE, n_jobs=-1)

        grid_search = GridSearchCV(
            estimator=xgb,
            param_grid=PARAM_GRID,
            cv=CV_FOLDS,
            scoring=SCORING_METRIC,
            verbose=2,
            n_jobs=-1
        )

        grid_search.fit(X_train, y_train)

        best_model = grid_search.best_estimator_
        best_params = grid_search.best_params_

        print(f"\n>>> BEST PARAMS: {best_params}")

        predicted_qualities = best_model.predict(X_test)
        (rmse, mae, r2) = eval_metrics(y_test, predicted_qualities)

        print(f"Winner Model Metrics:")
        print(f"  RMSE: {rmse}")
        print(f"  MAE: {mae}")
        print(f"  R2: {r2}")

        mlflow.log_params(best_params)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)

        print("Model is saving to Registry...")

        mlflow.sklearn.log_model(
            sk_model = best_model,
            artifact_path = "model",
            registered_model_name = MODEL_REGISTRY_NAME,
            input_example = X_train.head()
        )

        print(f"Model has successfully been registered to {MODEL_REGISTRY_NAME} with a new version")

if __name__ == "__main__":
    train_model()