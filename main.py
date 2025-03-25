import os
import sqlite3
import pandas as pd

DB_DIR = "./db"
DB_PATH = os.path.join(DB_DIR, "cell_database.db")
DATA_DIR = "./data"
DATA_FILE = "cell2info"
EXTRACTED_FILE = "cell2info.csv"

os.makedirs(DB_DIR, exist_ok=True)


def download_data():
    tsv_path = os.path.join(DATA_DIR, DATA_FILE)
    if os.path.exists(tsv_path):
        df = pd.read_csv(tsv_path, sep="\t")
        df.to_csv(os.path.join(DATA_DIR, EXTRACTED_FILE), index=False)
    else:
        print(
            f"Data file {tsv_path} does not exist. Please ensure the .tsv file is available."
        )


def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 테이블 생성 (제2정규형 적용)
    cursor.executescript(
        """
    CREATE TABLE IF NOT EXISTS cells (
        cell_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        taxonomy_id INTEGER,
        description TEXT,
        FOREIGN KEY (taxonomy_id) REFERENCES taxonomy (taxonomy_id)
    );

    CREATE TABLE IF NOT EXISTS taxonomy (
        taxonomy_id INTEGER PRIMARY KEY,
        classification TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS synonyms (
        row_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cell_id INTEGER NOT NULL,
        synonym TEXT NOT NULL,
        FOREIGN KEY (cell_id) REFERENCES cells (cell_id)
    );
    """
    )

    conn.commit()
    conn.close()
    print("Database setup complete.")


# 5. 데이터 삽입
def insert_data():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_csv(os.path.join(DATA_DIR, EXTRACTED_FILE))
    print(df.head())
    # df_cells = df[["CellID", "Name", "TaxonomyID", "description"]].drop_duplicates()
    # df_taxonomy = df[["taxonomy_id", "classification"]].drop_duplicates()
    # df_synonyms = df[["cell_id", "synonym"]].drop_duplicates()

    # df_cells.to_sql("cells", conn, if_exists="append", index=False)
    # df_taxonomy.to_sql("taxonomy", conn, if_exists="append", index=False)
    # df_synonyms.to_sql("synonyms", conn, if_exists="append", index=False)

    conn.commit()
    conn.close()
    print("Data insertion complete.")


# 실행 순서
if __name__ == "__main__":
    download_data()
    setup_database()
    insert_data()
