import mlflow
import shutil
import os
from pathlib import Path
from mlflow.tracking import MlflowClient
import warnings

# Uyarıları sustur (Kafa karıştırmasın)
warnings.filterwarnings("ignore")

# Config
from src.config import MLFLOW_TRACKING_URI, MODEL_REGISTRY_NAME


def fetch_best_model():
    print(f"1. MLflow'a bağlanılıyor: {MLFLOW_TRACKING_URI}")
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    client = MlflowClient()

    # --- Arama ---
    print(f"2. '{MODEL_REGISTRY_NAME}' aranıyor...")
    # Hata varsa direkt patlasın, try-except yok.
    versions = client.get_latest_versions(MODEL_REGISTRY_NAME, stages=["None", "Staging", "Production"])

    if not versions:
        print("!!! HATA: Registry boş! Hiç model versiyonu yok.")
        print("Lütfen önce 'python -m src.train' kodunu çalıştırıp bir model kaydettiğinden emin ol.")
        return

    # --- Seçim ---
    latest_model = max(versions, key=lambda x: int(x.version))
    print(f"3. Bulunan Model: Versiyon {latest_model.version}")
    print(f"   Durumu (Stage): {latest_model.current_stage}")
    print(f"   Kaynağı (Source URI): {latest_model.source}")

    # --- Hedef ---
    dest_path = Path("app/model_files")
    if dest_path.exists():
        print(f"4. Eski klasör temizleniyor: {dest_path}")
        shutil.rmtree(dest_path)

    # --- İndirme (Kritik An) ---
    # models:/DiamondsRegressor/2
    download_uri = f"models:/{MODEL_REGISTRY_NAME}/{latest_model.version}"
    print(f"5. İndirme Başlıyor... URI: {download_uri}")

    # Burada hata verirse, tam hatayı göreceğiz.
    mlflow.artifacts.download_artifacts(artifact_uri=download_uri, dst_path=str(dest_path))

    print("-" * 30)
    print(f"✅ BAŞARILI! Dosyalar şuraya indi: {dest_path.absolute()}")
    print("Klasörün içindekiler:")
    for f in dest_path.rglob("*"):
        print(f" - {f.name}")


if __name__ == "__main__":
    fetch_best_model()