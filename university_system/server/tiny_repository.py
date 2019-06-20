import tinydb
from tinydb import TinyDB

from university_system.server import json_converter


def it(key):
    return tinydb.where(key)


class TinyRepository:
    def __init__(self, db_path, table_name):
        self.db_file_name = db_path
        self.db = TinyDB(db_path)
        self.table_name = table_name
        self.table = self.db.table(table_name)

    def clear(self):
        self.db.purge_table(self.table_name)

    def add(self, obj):
        dic = json_converter.to_dict(obj)
        return self.table.insert(dic)

    def get(self, doc_id):
        return json_converter.to_object(self.table.get(doc_id=doc_id))

    def search(self, key, value=None, as_list=True):
        if isinstance(key, list):
            results = self.table.search(it(key[0]) == value[0] and it(key[1]) == value[1])
        else:
            results = self.table.search(it(key)) if value is None else self.table.search(it(key) == value)
        if len(results) > 0:
            return [json_converter.to_object(r) for r in results] if as_list else json_converter.to_object(results[0])
        else:
            return None

    def update(self, obj):
        self.table.write_back([obj])

    def delete(self, obj_id):
        self.table.remove(doc_ids=[obj_id])

    def __del__(self):
        self.db.close()
