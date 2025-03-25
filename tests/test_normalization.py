import sqlite3

def get_db_connection(db_path):
    conn = sqlite3.connect(db_path)
    return conn

def is_1nf(table_data):
    for row in table_data:
        for value in row:
            if isinstance(value, (list, dict, set)):
                return False
    return True

def is_2nf(table_name, table_data, primary_key, functional_dependencies):
    if not is_1nf(table_data):
        return False

    for fd in functional_dependencies:
        original_column, dependent_column = fd
        if original_column not in primary_key:
            return False

    return True


def get_table_data(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    return rows

def get_functional_dependencies(conn, table_name):
    if table_name == "cells":
        return [("CellID", "Name")]
    elif table_name == "taxonomy":
        return [("Organism", "TaxonomyID")]
    elif table_name == "synonyms":
        return [("RowID", "Synonyms")]
    return []


def test_is_2nf_cells():
    conn = get_db_connection("./db/cell_database.db")
    table_data = get_table_data(conn, "cells")
    primary_key = ["CellID"]
    functional_dependencies = get_functional_dependencies(conn, "cells")

    assert (
        is_2nf("cells", table_data, primary_key, functional_dependencies) == True
    ), "cells 테이블은 2NF를 만족해야 합니다."
    conn.close()


def test_is_2nf_taxonomy():
    conn = get_db_connection("./db/cell_database.db")
    table_data = get_table_data(conn, "taxonomy")
    primary_key = ["Organism"]
    functional_dependencies = get_functional_dependencies(conn, "taxonomy")

    assert (
        is_2nf("taxonomy", table_data, primary_key, functional_dependencies) == True
    ), "taxonomy 테이블은 2NF를 만족해야 합니다."
    conn.close()


def test_is_2nf_synonyms():
    conn = get_db_connection("./db/cell_database.db")
    table_data = get_table_data(conn, "synonyms")
    primary_key = ["RowID"]
    functional_dependencies = get_functional_dependencies(conn, "synonyms")

    assert (
        is_2nf("synonyms", table_data, primary_key, functional_dependencies) == True
    ), "synonyms 테이블은 2NF를 만족해야 합니다."
    conn.close()
