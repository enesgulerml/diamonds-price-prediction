# End-to-End Diamonds Price Prediction (v4.0)

This project implements a "Google-level" MLOps pipeline for regression tasks, predicting diamond prices based on their physical characteristics.

It features a sophisticated **MLflow Model Registry** workflow and an **Embedded Model** deployment strategy (CI/CD simulation), ensuring that the Docker container is self-sufficient, immutable, and production-ready.

* **v1.0: Engineering:** Data cleaning (IQR Outlier Removal) & Ordinal Encoding.
* **v2.0: Optimization:** XGBoost training with `GridSearchCV` and `MLflow Registry`.
* **v3.1: Serving:** A self-contained `FastAPI` container (Model baked-in).
* **v4.0: Demo:** A `Streamlit` dashboard acting as a client.

---

```
## 🚀 Project Structure

diamonds-price-prediction/
│
├── app/                  <- (v3.0) API service code
│   ├── __init__.py
│   ├── main.py           <- (API Motor - Loads embedded model from local dir)
│   ├── schemas.py        <- (Pydantic Contracts - Data Validation)
│   └── model_files/      <- (Artifacts downloaded by 'fetch_model.py' for Docker)
│
├── dashboard/            <- (v4.0) Streamlit dashboard code
│   └── app.py            <- (Client "Direksiyon" - Consumes API)
│
├── data/                 <- (Data Storage - Ignored by Git)
│   ├── raw/              <- (Raw CSV extracted from Seaborn)
│   └── processed/        <- (Cleaned & Ordinal Encoded CSV)
│
├── models/               <- (Local Model Storage - Ignored by Git)
│
├── src/                  <- (v1.0 & v2.0) Engineering & Training logic
│   ├── __init__.py
│   ├── config.py         <- (Central Configuration & Search Space)
│   ├── data_processing.py<- (IQR Cleaning & Ordinal Encoding)
│   ├── train.py          <- (GridSearch Training & Registry Logging)
│   └── fetch_model.py    <- (CI/CD Script: Fetches model from Registry for Build)
│
├── .dockerignore         <- (Ensures clean Docker context)
├── .gitignore            <- (Git exclusions)
├── requirements.txt      <- (v5 Strategy: Single source of truth)
├── Dockerfile            <- (v5 Strategy: Pip-optimized & Embedded Model)
└── README.md             <- (The project user manual)
```

---

## 🛠️ Installation & Setup

Follow these steps to set up the project environment on your local machine.

### 1. Clone the Repository
```bash
git clone https://github.com/enesgulerml/diamonds-price-prediction.git
cd diamonds-price-prediction
```

### 2. Setup Environment (v5 Strategy)
We use conda for Python management and pip for package management to avoid solver issues.

```bash
conda create -n diamonds-registry python=3.10 -y
conda activate diamonds-registry
pip install -r requirements.txt
pip install -e .
```

### 3. Extract Data
Since the dataset comes from Seaborn, run this one-liner to save it locally:

```bash
python -c "import seaborn as sns; import os; os.makedirs('data/raw', exist_ok=True); sns.load_dataset('diamonds').to_csv('data/raw/diamonds.csv', index=False); print('Data extracted.')"
```

## ⚡ Workflow & Usage
This project follows a strict Train -> Build -> Serve lifecycle.

### Phase 1: Train & Register (v2.0)
This step cleans the data, runs a GridSearchCV to find the best XGBoost parameters, and registers the winning model to your local MLflow Registry.

#### 1. Start MLflow Server (Terminal 1): Keep this terminal open.
```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlartifacts --host 0.0.0.0 --port 5000
```

#### 2. Run Training (Terminal 2):
```bash
python -m src.train
```
Check results at http://127.0.0.1:5000

### Phase 2: Build the API Image (CI/CD Simulation)
Unlike typical setups, we do not mount the model volume at runtime. We fetch it first and bake it into the Docker image. This makes the container immutable.

1. **Fetch Model:** This script connects to the Registry, downloads the latest 'Production' (or newest) model, and places it in app/model_files/.

```bash
python -m src.fetch_model
```

2. **Build Docker Image:** The Dockerfile will copy the app/model_files/ folder into the image.

```bash
docker build -t diamonds-api:v4 .
```

### Phase 3: Serve & Demo (v3.1 + v4.0)
Now you can run the self-contained API and the Dashboard.

1. **Run API Motor (Terminal 2):** The container runs on port 8005 to avoid conflicts. It needs NO external volumes or database connections.

```bash
docker run -d --rm -p 8005:80 diamonds-api:v4
```
Verify API Docs: http://localhost:8005/docs

2. **Run Dashboard (Terminal 3):** This launches the Streamlit interface that talks to the API.

```bash
streamlit run dashboard/app.py
```
Open Dashboard: http://localhost:8501
