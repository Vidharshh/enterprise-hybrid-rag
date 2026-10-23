import os
import glob
import pandas as pd
from sqlalchemy import create_engine

# Database credentials (matching your .env)
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "olist_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def load_csvs_to_postgres():
    engine = create_engine(DATABASE_URL)
    data_dir = "data/raw"
    
    # Recursively find all CSV files inside data/raw
    csv_files = glob.glob(f"{data_dir}/**/*.csv", recursive=True)
    
    if not csv_files:
        print(f"❌ No CSV files found in {data_dir}. Ensure files are unzipped there!")
        return

    print(f"📦 Found {len(csv_files)} CSV files to load...")

    for file in csv_files:
        filename = os.path.basename(file)
        # Standardize table names e.g. 'olist_customers_dataset.csv' -> 'customers'
        table_name = filename.replace("olist_", "").replace("_dataset.csv", "").replace(".csv", "")
        
        print(f"⏳ Loading {filename} into table '{table_name}'...")
        df = pd.read_csv(file)
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        print(f"✅ Loaded {len(df)} rows into '{table_name}'.")

    print("\n🎉 All Olist dataset tables loaded into Postgres container successfully!")

if __name__ == "__main__":
    load_csvs_to_postgres()