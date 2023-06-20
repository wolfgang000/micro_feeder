import os
from urllib.parse import urlparse
import psycopg

database_url = os.environ["DATABASE_URL"]
parsed_db_url = urlparse(database_url)
db_username = parsed_db_url.username
db_password = parsed_db_url.password
database = parsed_db_url.path[1:]
db_hostname = parsed_db_url.hostname
db_port = parsed_db_url.port


def sql_connect():
    return psycopg.connect(
        "dbname={} user={} password={} port={} host={}".format(
            "postgres_dev", db_username, db_password, db_port, db_hostname
        )
    )
