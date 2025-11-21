import seaborn as sns
import os

def extract():
    os.makedirs("data/raw", exist_ok=True)
    df = sns.load_dataset("diamonds")
    df.to_csv("data/raw/diamonds.csv", index=False)
    print("Data saved to 'data/raw/diamonds.csv'")

if __name__ == "__main__":
    extract()