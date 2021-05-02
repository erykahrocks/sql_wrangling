from psycopg2 import extras

import argparse
import psycopg2

from main import connect

def execute_query(prob: str):

    cursor_dict = {
        'cursor_factory': psycopg2.extras.NamedTupleCursor
    }

    conn = connect(**cursor_dict)

    ddl_sql = open(f'sql/{prob}.sql', 'r').read()
    with conn, conn.cursor() as cur:
        cur.execute(ddl_sql)
        for row in cur.fetchall():
            print(row)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Specify problem num')
    parser.add_argument('--prob', type=str, required=True)
    args = parser.parse_args()

    execute_query(prob=args.prob)