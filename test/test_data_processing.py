import pytest
import pandas as pd
import numpy as np
from src.data_processing import remove_outliers
from src.config import OUTLIER_COLUMNS


def test_remove_outliers():
    """
    Test v5.1 (Unit Test):
    Validates that the IQR outlier removal logic actually removes extreme values.
    """
    # Arrange: Create a dummy DataFrame with a clear outlier
    data = {
        "carat": [1.0, 1.1, 1.0, 1.2, 50.0],
        "depth": [60, 61, 62, 61, 60],
        "table": [55, 56, 55, 57, 55],
        "x": [5, 5, 5, 5, 5],
        "y": [5, 5, 5, 5, 5],
        "z": [3, 3, 3, 3, 3],
        "price": [5000, 5100, 5050, 5200, 99999]
    }
    df = pd.DataFrame(data)

    assert "carat" in OUTLIER_COLUMNS

    # Act
    df_clean = remove_outliers(df)

    # Assert
    assert len(df_clean) == 4
    assert 50.0 not in df_clean["carat"].values