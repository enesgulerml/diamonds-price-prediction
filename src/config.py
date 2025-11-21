import os
from pathlib import Path

# File Path
SRC_ROOT = Path(__file__).parent
PROJECT_ROOT = SRC_ROOT.parent

# Data Path
DATA_DIR = PROJECT_ROOT / 'data'
RAW_DATA_PATH = DATA_DIR / "raw" / "diamonds.csv"
PROCESSED_DATA_PATH = DATA_DIR / "processed" / "diamonds_processed.csv"

# Model Path
MODELS_DIR = PROJECT_ROOT / 'models'
MODEL_PATH = MODELS_DIR / 'model.joblib'

def ensure_directories():
    """Be sure critical directories are created."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "raw").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "processed").mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

ensure_directories()

# MLflow & Registry Settings
MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
MLFLOW_EXPERIMENT_NAME = "Diamonds Price Prediction"

MODEL_REGISTRY_NAME = "DiamondsRegressor"

# Data Columns
TARGET = "price"
NUMERICAL_FEATURES = ["carat", "depth", "table", "x", "y", "z"]
CATEGORICAL_FEATURES = ["cut","color","clarity"]

# Outlier Settings
OUTLIER_COLUMNS = ["carat","depth","table","x","y","z"]

IQR_THRESHOLD = 1.5

# Ordinal Mapping
CUT_ORDER = ["Fair","Good","Very Good","Premium","Ideal"]
COLOR_ORDER = ["J","I","H","G","F","E","D"]
CLARITY_ORDER = ["I1","SI2","SI1","VS2","VS1","VVS2","VVS1","IF"]


# Train Settings
TEST_SIZE = 0.2
RANDOM_STATE = 42

# Hyperparameter Settings
PARAM_GRID = {
    "n_estimators": [100, 300, 500],
    "max_depth": [3, 6],
    "learning_rate": [0.05, 0.1],
    "subsample": [0.8, 1.0]
}

CV_FOLDS = 3
SCORING_METRIC = "neg_root_mean_squared_error"