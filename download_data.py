import os
import sys
import urllib.request
import time

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DATA_URL = "https://raw.githubusercontent.com/Helmy2/Diabetes-Health-Indicators/main/diabetes_binary_health_indicators_BRFSS2015.csv"
OUTPUT_FILE = os.path.join(DATA_DIR, "diabetes_data.csv")

def download_dataset():
    os.makedirs(DATA_DIR, exist_ok=True)
    
    if os.path.exists(OUTPUT_FILE) and os.path.getsize(OUTPUT_FILE) > 20 * 1024 * 1024:
        print(f"[OK] Dataset already exists at {OUTPUT_FILE} ({os.path.getsize(OUTPUT_FILE) / (1024*1024):.2f} MB). Skipping download.")
        return OUTPUT_FILE

    print(f"[*] Starting download from: {DATA_URL}")
    print(f"[*] Target destination: {OUTPUT_FILE}")
    start_time = time.time()

    def report_progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            percent = downloaded * 100 / total_size
            speed = (downloaded / (1024 * 1024)) / (time.time() - start_time + 1e-5)
            sys.stdout.write(f"\rDownloading: {percent:5.1f}% | {downloaded / (1024 * 1024):.2f} / {total_size / (1024 * 1024):.2f} MB | {speed:.2f} MB/s")
            sys.stdout.flush()

    try:
        urllib.request.urlretrieve(DATA_URL, OUTPUT_FILE, reporthook=report_progress)
        print("\n[OK] Download completed successfully!")
    except Exception as e:
        print(f"\n[ERROR] Download failed: {e}")
        raise

    file_size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    print(f"[+] Verified file size: {file_size_mb:.2f} MB")
    
    # Quick row count check
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        row_count = sum(1 for _ in f) - 1
    print(f"[+] Total records loaded: {row_count:,} patient rows")
    return OUTPUT_FILE

if __name__ == "__main__":
    download_dataset()
