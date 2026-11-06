import os
import pandas as pd

# --- 1. MEMBACA DATASET DENGAN PATH OTOMATIS ---
base_dir = os.path.dirname(os.path.abspath(__file__))
# Mengakses folder data yang berada satu tingkat di luar folder notebooks
file_path = os.path.abspath(
    os.path.join(base_dir, "..", "data", "rawday.csv")
)

print(f"=== 1. MEMBACA DATASET STEAM GAMES ({file_path}) ===")
df = pd.read_csv(file_path)
df.columns = df.columns.str.strip().str.lower()

print("Jumlah Baris & Kolom:", df.shape)
print("\nJumlah Missing Value per Kolom:")
print(df.isnull().sum())

# --- 2. PERHITUNGAN STATISTIK DESKRIPTIF ---
print("\n=== 2. STATISTIK DESKRIPTIF NUMERIK ===")
num_df = df.select_dtypes(include=["number"])
print(num_df.describe().T)

# --- 3. ANALISIS PER TAHUN ---
if "release_year" in df.columns:
  print("\n=== 3. JUMLAH GAME PER TAHUN RILIS ===")
  print(df["release_year"].value_counts().sort_index())