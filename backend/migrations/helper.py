from sqlalchemy import text


def get_sql_content(file_path):
    with open(file_path) as f:
        return f.read()


def exec_sql(conn, file_path):
    content = get_sql_content(file_path)
    conn.execute(text(content))
