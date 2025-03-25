import sqlite3
import pandas as pd

def get_db_connection(db_path):
    """SQLite 데이터베이스 연결을 반환하는 함수"""
    return sqlite3.connect(db_path)

def load_db_to_dataframe(db_path, table_name):
    """DB에서 데이터를 불러와 DataFrame으로 반환하는 함수"""
    conn = get_db_connection(db_path)
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_table_data(conn, table_name):
    """DB에서 데이터를 불러와 리스트로 반환하는 함수"""
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    return rows

def is_1nf(table_data):
    """1NF를 만족하는지 확인하는 함수"""
    for row in table_data:
        for value in row:
            if isinstance(value, (list, dict, set)):
                return False
    return True

def is_2nf(df, pk_candidates):
    """2NF를 만족하는지 확인하는 함수"""
    if len(pk_candidates) <= 1:
        return True

    for pk_candidate in pk_candidates:
        for col in df.columns:
            if col not in pk_candidates:
                grouped = df.groupby(pk_candidate)[col].nunique()
                if grouped.max() <= 1:
                    return False
    return True

def run_test(table_name, primary_key, db_path):
    """테이블에 대해 1NF와 2NF를 테스트하는 함수"""
    conn = get_db_connection(db_path)
    table_data = get_table_data(conn, table_name)
    df = load_db_to_dataframe(db_path, table_name)

    assert is_1nf(table_data) == True, f"{table_name} 테이블은 1NF를 만족해야 합니다."
    assert is_2nf(df, primary_key) == True, f"{table_name} 테이블은 2NF를 만족해야 합니다."

    conn.close()

def test_is_2nf_cells():
    """cells 테이블에 대한 테스트"""
    run_test("cells", ["CellID"], "./db/cell_database.db")

def test_is_2nf_taxonomy():
    """taxonomy 테이블에 대한 테스트"""
    run_test("taxonomy", ["TaxonomyID", "Name"], "./db/cell_database.db")

def test_is_2nf_synonyms():
    """synonyms 테이블에 대한 테스트"""
    run_test("synonyms", ["RowID"], "./db/cell_database.db")
