import pytest
import requests
import subprocess
import time
import os
from pathlib import Path

# Configuration
IMAGE_NAME = "diamonds-api:v4"
CONTAINER_NAME = "test_diamonds_api"
API_PORT = 8006
API_URL = f"http://127.0.0.1:{API_PORT}"
PREDICT_URL = f"{API_URL}/predict"


@pytest.fixture(scope="module")
def api_service():
    """
    v5.3 Fixture: Starts the Docker container (Embedded Model) for testing.
    """
    print(f"\n[Setup] Starting Docker container '{IMAGE_NAME}'...")

    # Run without volumes
    start_command = [
        "docker", "run",
        "-d", "--rm",
        "--name", CONTAINER_NAME,
        "-p", f"{API_PORT}:80",
        IMAGE_NAME
    ]

    try:
        subprocess.run(start_command, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to start Docker. Is '{IMAGE_NAME}' built? Error: {e.stderr.decode()}")

    time.sleep(5)

    # Health Check
    retries = 5
    for i in range(retries):
        try:
            requests.get(f"{API_URL}/")
            print("[Setup] Health check passed.")
            break
        except requests.exceptions.ConnectionError:
            if i == retries - 1:
                subprocess.run(["docker", "stop", CONTAINER_NAME])
                pytest.fail("Could not connect to API.")
            time.sleep(2)

    yield PREDICT_URL

    print(f"\n[Teardown] Stopping container...")
    subprocess.run(["docker", "stop", CONTAINER_NAME], capture_output=True)


@pytest.mark.slow
def test_api_prediction(api_service):
    """
    Test v5.3 (E2E): Sends a diamond payload and checks for a price.
    """
    payload = {
        "carat": 1.0,
        "cut": "Ideal",
        "color": "E",
        "clarity": "SI1",
        "depth": 61.5,
        "table": 55.0,
        "x": 6.5,
        "y": 6.5,
        "z": 4.0
    }

    response = requests.post(api_service, json=payload)

    assert response.status_code == 200
    data = response.json()

    assert "predicted_price" in data
    assert isinstance(data["predicted_price"], float)
    assert data["predicted_price"] > 0
    assert "model_version" in data