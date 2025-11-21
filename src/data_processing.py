import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
import sys

from src.config import (
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH,
    TARGET,
    CUT_ORDER,
    COLOR_ORDER,
    CLARITY_ORDER,
    TEST_SIZE,
    RANDOM_STATE,
    OUTLIER_COLUMNS,
    IQR_THRESHOLD
)

def remove_outliers(df):
    """
    Removes outliers using the IQR method for the columns specified in Config.
    """
    df_clean = df.copy()
    print("Removing outliers...")

    initial_rows = len(df_clean)

    for col in OUTLIER_COLUMNS:
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - (IQR_THRESHOLD * IQR)
        upper_bound = Q3 + (IQR_THRESHOLD * IQR)

        df_clean = df_clean[
            (df_clean[col] >= lower_bound) &
            (df_clean[col] <= upper_bound)
            ]

        lost_rows = initial_rows - len(df_clean)
        print(f"Outlier cleaning has finished with {lost_rows} rows.")
        return df_clean

def load_and_process_data():
    """
    Loads data, makes ordinal encoding and saves processed data.
    """
    print("Data Processing Starting...")

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"{RAW_DATA_PATH} does not exist")

    df = pd.read_csv(RAW_DATA_PATH)

    df = df[(df[["x","y","z"]] != 0).all(axis=1)]

    df = remove_outliers(df)

    encoder = OrdinalEncoder(categories=[CUT_ORDER, COLOR_ORDER, CLARITY_ORDER])

    df[["cut","color","clarity"]] = encoder.fit_transform(
        df[["cut","color","clarity"]]
    )

    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Processed data saved to {PROCESSED_DATA_PATH}")

    return df

def get_train_test_split():
    df = load_and_process_data()

    X = df.drop(columns=[TARGET])
    y = df[TARGET]

    return train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE)

if __name__ == "__main__":
    load_and_process_data()