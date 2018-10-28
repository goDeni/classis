# -*- coding: utf-8 -*-

import sqlite3
from typing import Tuple

from classis.utils import is_valid_name

DATABASE_PATH = "database.sqlite"
MAIN_TABLE_NAME = "MAIN_LIST"


def create_connection(db_path=DATABASE_PATH):
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
    except sqlite3.Error as e:
        print(e)
    return conn


def database_cursor(func):
    def wrapper(*args, **kwargs):
        conn = create_connection()
        if conn is None:
            return
        cursor = conn.cursor()
        res = func(cursor, *args, **kwargs)

        conn.commit()
        cursor.close()
        conn.close()
        return res
    return wrapper


@database_cursor
def init_database(cursor: sqlite3.Cursor):
    cursor.execute("""
    create table if not exists {table_name} (
        ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        PARENT_ID INTEGER NOT NULL ,
        NAME CHAR(100) NOT NULL, 
        THIS_LIST boolean NOT NULL
    );""".format(table_name=MAIN_TABLE_NAME))


@database_cursor
def add_element(cursor: sqlite3.Cursor, name: str, this_list: bool, parent_id=0) -> Tuple[int, str]:
    if not is_valid_name(name):
        return 0, "Invalid name"

    res = cursor.execute("SELECT COUNT(*) FROM {table_name} WHERE PARENT_ID = {parent_id} AND NAME = '{name}';".format(
        table_name=MAIN_TABLE_NAME,
        name=name,
        parent_id=parent_id,
    )).fetchone()[0]
    if res:
        return 0, "This name already use"

    query = """
        INSERT INTO {table_name} (PARENT_ID, NAME, THIS_LIST) 
        VALUES ({parent_id}, '{name}', {THIS_LIST});
        """.format(
            table_name=MAIN_TABLE_NAME,
            name=name,
            THIS_LIST=int(this_list),
            parent_id=parent_id,
        )
    if not parent_id:
        cursor.execute(query)
        return 1, ''

    parent_element = read_element(cursor, parent_id)
    if not parent_element:
        return 0, "Invalid key 'parent_id'"

    if not parent_element[1]:
        return 0, "Parent is not list"

    cursor.execute(query)
    return 1, ''


def read_element(cursor: sqlite3.Cursor, element_id: int):
    return cursor.execute("""
    SELECT NAME, THIS_LIST, PARENT_ID FROM {table_name}
    WHERE ID == {element_id};
    """.format(
        table_name=MAIN_TABLE_NAME,
        element_id=element_id,
    )).fetchone()


@database_cursor
def read_table(cursor: sqlite3.Cursor, parent_id=0):
    parent_el = read_element(cursor, parent_id)
    if parent_el is None and parent_id != 0:
        return 0, "Invalid parent_id"
    data = cursor.execute("""
    SELECT ID, NAME, THIS_LIST 
    FROM {table_name} where PARENT_ID={parent_id}
    ORDER BY THIS_LIST DESC, name ASC;
    """.format(
        table_name=MAIN_TABLE_NAME,
        parent_id=parent_id,
    )).fetchall()
    return {
        'items': [[id_, name, bool(this_list)] for id_, name, this_list in data],
        'count': len(data),
    }


def is_list_element(cursor: sqlite3.Cursor, element_id: int) -> bool:
    element = read_element(cursor, element_id)
    return element is None or bool(element[1]) or element_id == 0


@database_cursor
def update_element(cursor: sqlite3.Cursor, element_id: int, name: str, parent_id: int):
    element = read_element(cursor, element_id)
    if not element:
        return 0, "Invalid element_id"
    element_name, this_list, element_parent_id = element
    if name is not None and is_valid_name(name):
        element_name = name
    if parent_id is not None:
        if not is_list_element(cursor, parent_id) or parent_id == element_id or (this_list and str(parent_id) in get_lists_in_list(cursor, element_id)):
            return 0, "Invalid parent_id"
        element_parent_id = parent_id
    cursor.execute("""
    UPDATE {table_name}
    SET NAME = '{new_name}', PARENT_ID = {new_parent_id}
    WHERE ID = {element_id}
    ;""".format(
        table_name=MAIN_TABLE_NAME,
        new_name=element_name,
        new_parent_id=element_parent_id,
        element_id=element_id,
    ))
    return 1, None


def get_lists_in_list(cursor: sqlite3.Cursor, element_id) -> list:
    parent_ids = [str(element_id)]
    for parent_id in parent_ids:
        res = cursor.execute("""
            SELECT ID FROM {table_name}
            WHERE THIS_LIST == 1 AND PARENT_ID = {parent_id}
        ;""".format(
            table_name=MAIN_TABLE_NAME,
            parent_id=parent_id,
        )).fetchall()
        if not res:
            break
        parent_ids += [str(a[0]) for a in res]
    return parent_ids


@database_cursor
def delete_element(cursor: sqlite3.Cursor, element_id: int):
    element = read_element(cursor, element_id)
    if not element:
        return 0, "Invalid element_id"
    if not element[1]:
        cursor.execute("""
        DELETE FROM {table_name}
        WHERE ID = {element_id}
        ;""".format(
            table_name=MAIN_TABLE_NAME,
            element_id=element_id,
        ))
        return 1, None
    delete_parents_ids = get_lists_in_list(cursor, element_id)

    cursor.execute("""
        DELETE FROM {table_name}
        WHERE PARENT_ID IN {delete_ids} OR ID = {element_id}
    ;""".format(
        table_name=MAIN_TABLE_NAME,
        delete_ids="({})".format(','.join(delete_parents_ids)),
        element_id=element_id,
    ))
    return 1, None
