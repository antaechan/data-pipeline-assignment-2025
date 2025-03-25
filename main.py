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
        df.to_csv(os.path.join(DATA_DIR, EXTRACTED_FILE))
    else:
        print(
            f"Data file {tsv_path} does not exist. Please ensure the .tsv file is available."
        )


def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.executescript(
        """
    DROP TABLE IF EXISTS cells;
    DROP TABLE IF EXISTS taxonomy;
    DROP TABLE IF EXISTS synonyms;

    CREATE TABLE cells (
        CellID INTEGER PRIMARY KEY,
        Name TEXT,
        Tissue TEXT,
        Organism TEXT,
        TaxonomyID INTEGER,
        Synonyms TEXT
    );

    CREATE TABLE taxonomy (
        TaxonomyID INT,
        Name TEXT,
        Organism TEXT,
        PRIMARY KEY (TaxonomyID, Name)
    );

    CREATE TABLE synonyms (
        RowID INTEGER PRIMARY KEY AUTOINCREMENT,
        Synonyms TEXT
    );
    """
    )

    conn.commit()
    conn.close()
    print("Database setup complete.")

def insert_data():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_csv(os.path.join(DATA_DIR, EXTRACTED_FILE))
    df_cells = df[["CellID", "Name", "Tissue", "Organism", "TaxonomyID", "Synonyms"]].drop_duplicates()
    df_taxonomy = df[["TaxonomyID", "Name", "Organism"]].drop_duplicates()
    df_synonyms = df[["Synonyms"]].drop_duplicates()

    df_cells.to_sql("cells", conn, if_exists="append", index=False)
    df_taxonomy.to_sql("taxonomy", conn, if_exists="append", index=False)
    df_synonyms.to_sql("synonyms", conn, if_exists="append", index=False)

    conn.commit()
    conn.close()
    print("Data insertion complete.")

if __name__ == "__main__":
    download_data()
    setup_database()
    insert_data()
