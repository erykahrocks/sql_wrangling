from string import Template
from typing import Tuple, Union, DefaultDict

import logging
import psycopg2
import uuid

from config import config
from preprocess import get_personal_info, get_medical_info

MY_SCHEMA = {
    'schema': 'walker101'
}

MAX_TRY = 3

logger = logging.getLogger()

def _record_to_string(record: Tuple) -> str:
    return record[0]

def _generate_random_bigint() -> int:
    return uuid.uuid4().int & (1<<63)-1

def _insert_with_pk(table: DefaultDict[str, str], table_name: str, conn) -> Union[None, int]:
    pk_val = None
    pk = table_name + '_id'
    query_template = Template(open(f'sql/insert/{table_name}.sql').read())

    # table could be empty
    if not table:
        logger.warning(f'Skipping {table_name}')
        return pk_val

    for _ in range(MAX_TRY):
        pk_val = _generate_random_bigint()
        table[pk] = pk_val

        record_insert = query_template.substitute(**MY_SCHEMA, **table)
        with conn, conn.cursor() as cur:
            try:
                cur.execute(record_insert)
                break
            except psycopg2.DatabaseError as e:
                logger.error(e)
                # UniqueKeyViolation
                if e.pgcode == '23505':
                    logger.error("Go buy some lottery!")
                pk_val = None
                continue
    if pk_val is None:
        logger.error(f"Insertion to {table_name} failed with {MAX_TRY} retries")
        raise RuntimeError
    return pk_val

def connect(**kwargs):
    """ Connect to the PostgreSQL database server """
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        logger.info('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params, **kwargs)

        conn.autocommit = True

        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        raise error


def main():
    conn = connect()

    for table in ['person',  'visit_occurrence', 'condition_occurrence', 'drug_exposure']:
        ddl_sql = open(f'sql/ddl/{table}.sql', 'r').read()
        ddl_sql = Template(ddl_sql).substitute(**MY_SCHEMA)
        with conn, conn.cursor() as cur:
            cur.execute(ddl_sql)

    note_fetch_sql = """
    SELECT note
    FROM de.clinical_note
    """
    with conn, conn.cursor() as cur:
        cur.execute(note_fetch_sql)
        records = cur.fetchall()

    # fishy part
    pseudo_user_id_map = {}
    for record in map(_record_to_string, records):
        personal_info = get_personal_info(record)
        pseudo_user_id = personal_info['pseudo_user_id']
        # duplicated user. No insertion needed
        if pseudo_user_id in pseudo_user_id_map:
            person_pk = pseudo_user_id_map[pseudo_user_id]
        else:
            person_pk = _insert_with_pk(personal_info, 'person', conn)
            if person_pk is None:
                logger.error('Person relation must be non-empty')
                raise AssertionError
            pseudo_user_id_map[pseudo_user_id] = person_pk

        vo, de, co = get_medical_info(record)
        # setting foreign key
        vo['person_id'] = person_pk
        vo_pk = _insert_with_pk(vo, 'visit_occurrence', conn)
        if vo_pk is None:
            logger.error('Visit occurrence relation must be non-empty')
            raise AssertionError

        # setting foreign key again
        # could be empty table
        for table, name in zip(
                [de,co], ['drug_exposure', 'condition_occurrence']):
            if not table:
                logger.warning(f'Skipping table {name}')
                continue
            table['person_id'] = person_pk
            table['visit_occurrence_id'] = vo_pk
            _insert_with_pk(table, name, conn)

if __name__ == '__main__':
    main()
