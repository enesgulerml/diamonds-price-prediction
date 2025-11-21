# ⚠️ Troubleshooting Guide

This document outlines common environment-specific issues encountered during setup, building, or testing, along with their solutions.

---

## 1. Docker Build Fails: `cannot allocate memory` or `Killed`

**Symptom:**
When running `docker build ...`, the process terminates unexpectedly during package installation (`RUN pip install` or `RUN conda env update`) with errors such as:
* `Solving environment: \ Killed`
* `ERROR: ... cannot allocate memory`
* `subprocess.CalledProcessError: Command ... returned non-zero exit status 137`
* `Segmentation fault (core dumped)`

**Cause:**
This is an **infrastructure configuration issue**. Dependency solvers (especially Conda or heavy pip builds like XGBoost/Surprise) can consume significant RAM (>6GB). The default memory limit for Docker Desktop on WSL 2 (Windows) is often set too low (e.g., 2GB or 4GB) to handle this operation.

**Solution (Windows + WSL 2 Users):**
You must increase the memory allocated to the WSL 2 utility VM.

1.  Open a text editor (e.g., Notepad).
2.  Paste the following configuration (adjust `memory` based on your system, e.g., `8GB` or `10GB`):
    ```ini
    [wsl2]
    memory=10GB
    ```
3.  Save the file as **`.wslconfig`** in your user home directory:
    * Path: `C:\Users\[YourUsername]\.wslconfig`
4.  **Restart WSL 2 completely** for changes to take effect. Open PowerShell and run:
    ```powershell
    wsl --shutdown
    ```
5.  Restart **Docker Desktop**.
6.  Run the build command again.

---

## 2. Docker Build Fails: `gcc failed` or `Failed building wheel`

**Symptom:**
During `docker build`, the `pip install` step fails with:
* `error: command 'gcc' failed: No such file or directory`
* `ERROR: Failed building wheel for scikit-surprise`

**Cause:**
The project uses a lightweight base image (`python:3.10-slim`) to keep container size down. However, libraries like `scikit-surprise` or `xgboost` require C/C++ compilers to build from source, which are not included in "slim" images by default.

**Solution:**
Ensure you are using the latest **Dockerfile** provided in the repository. It includes the necessary build tools:

```dockerfile
# The Dockerfile fixes this by installing build-essential before pip install
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
```

## 3. Local Installation Fails: Microsoft Visual C++ 14.0 is required
**Symptom:** When running pip install -r requirements.txt directly on a Windows machine (not via Docker), the installation fails with:
* error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools"

**Cause:** Similar to issue #2, libraries like scikit-surprise need to compile C++ code. On Windows, this requires the Microsoft C++ compiler, which is likely missing.

**Solution:**
1. Download the [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/tr/visual-cpp-build-tools/).
2. Run the installer and select the "Desktop development with C++" workload.
3. Install and restart your computer.
4. Run pip install -r requirements.txt again.

## 4. Pytest E2E Fails: Unable to find image
**Symptom:** When running python -m pytest, the End-to-End (E2E) tests (test/test_api_e2e.py) fail with:
* subprocess.CalledProcessError
* docker: Error response from daemon: pull access denied for diamonds-api
* Unable to find image 'diamonds-api:v4' locally

**Cause:** The E2E tests attempt to spin up the Docker container to test the API. However, the tests assume the Docker image has already been built. They do not build the image for you.

**Solution:** You must build the Docker image manually before running the test suite.

1. Build the image:
```bash
docker build -t diamonds-api:v4 .
```

2. Run the tests:
```bash
python -m pytest
```