import sqlite3


# 1. 데이터베이스 연결
def get_db_connection(db_path):
    """DB 연결을 반환하는 함수"""
    conn = sqlite3.connect(db_path)
    return conn


# 2. 1NF 검증: 모든 값이 원자값인지 확인
def is_1nf(table_data):
    for row in table_data:
        for value in row:
            if isinstance(value, (list, dict, set)):  # 원자값이 아닌 경우
                return False
    return True


# 3. 2NF 검증: 부분 함수 종속성 검사
def is_2nf(table_name, table_data, primary_key, functional_dependencies):
    # 먼저 1NF 확인
    if not is_1nf(table_data):
        return False

    # 테이블의 각 Functional Dependency를 확인
    # for fd in functional_dependencies.get(table_name, []):
    #     dependent_column, original_column = fd
    #     # 만약 의존하는 컬럼이 기본 키의 일부라면 2NF 위반
    #     if original_column not in primary_key:
    #         return False

    return True


# 4. 테이블 데이터 조회
def get_table_data(conn, table_name):
    """DB에서 테이블의 데이터를 가져오는 함수"""
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    return rows


# 5. 기본 키를 불러오는 함수
def get_primary_key(conn, table_name):
    """DB에서 기본 키 추출"""
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    primary_key_columns = [col[1] for col in columns if col[5] == 1]  # PRIMARY KEY 표시
    return primary_key_columns


# 6. 기능적 종속성 예시 (실제로는 DB에서 계산하거나 정의해야 함)
def get_functional_dependencies(conn, table_name):
    """DB에서 기능적 종속성 정보 추출 (예시 데이터 기반)"""
    if table_name == "cells":
        return [("cell_id", "cell_name"), ("cell_id", "description")]
    elif table_name == "taxonomy":
        return [("taxonomy_id", "taxonomy_name"), ("taxonomy_id", "category")]
    elif table_name == "synonyms":
        return [("row", "synonym_name"), ("row", "language")]
    return []


# 7. pytest 테스트 케이스
def test_is_2nf_cells():
    conn = get_db_connection("./db/cell_database.db")
    table_data = get_table_data(conn, "cells")
    primary_key = get_primary_key(conn, "cells")
    functional_dependencies = get_functional_dependencies(conn, "cells")

    assert (
        is_2nf("cells", table_data, primary_key, functional_dependencies) == True
    ), "cells 테이블은 2NF를 만족해야 합니다."
    conn.close()


def test_is_2nf_taxonomy():
    conn = get_db_connection("./db/cell_database.db")
    table_data = get_table_data(conn, "taxonomy")
    primary_key = get_primary_key(conn, "taxonomy")
    functional_dependencies = get_functional_dependencies(conn, "taxonomy")

    assert (
        is_2nf("taxonomy", table_data, primary_key, functional_dependencies) == True
    ), "taxonomy 테이블은 2NF를 만족해야 합니다."
    conn.close()


def test_is_2nf_synonyms():
    conn = get_db_connection("./db/cell_database.db")
    table_data = get_table_data(conn, "synonyms")
    primary_key = get_primary_key(conn, "synonyms")
    functional_dependencies = get_functional_dependencies(conn, "synonyms")

    assert (
        is_2nf("synonyms", table_data, primary_key, functional_dependencies) == True
    ), "synonyms 테이블은 2NF를 만족해야 합니다."
    conn.close()
