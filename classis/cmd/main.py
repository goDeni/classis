# -*- coding: utf-8 -*-

from flask import Flask, request

from classis.utils_db import init_database, add_element, read_table, update_element, delete_element
from classis.utils import generate_response, integer_try_parse
app = Flask(__name__)

# headers={'Content-Type': 'application/json'}


@app.route('/list/', methods=['GET'])
@generate_response
def list_get():
    return read_table()


@app.route('/list/<int:element_id>', methods=['GET'])
@generate_response
def list_get_element(element_id: int):
    return read_table(parent_id=element_id)


@app.route('/list/', methods=['PUT'])
@generate_response
def list_put():
    data = request.json  # type: dict
    name = data.get('name', '')
    parent_id = integer_try_parse(data.get('parent_id'), 0)
    this_list = bool(data.get('this_list', False))
    res, err = add_element(name=name, parent_id=parent_id, this_list=this_list)
    return res, err


@app.route('/list/<int:element_id>', methods=['POST'])
@generate_response
def list_edit(element_id: int):
    data = request.json  # type: dict
    name = data.get('name')
    parent_id = data.get('parent_id')
    res, err = update_element(element_id=element_id, name=name, parent_id=parent_id)
    return res, err


@app.route('/list/<int:element_id>', methods=['DELETE'])
@generate_response
def list_delete(element_id: int):
    return delete_element(element_id=element_id)


def main():
    init_database()
    app.run(port=5000, host='0.0.0.0')


if __name__ == '__main__':
    main()
