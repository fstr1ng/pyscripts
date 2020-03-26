import functools
import sqlite3

class DBController:
    def __init__(self, db_path):
        self.db_path=db_path

    def _crud_method(f):
        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            self._db = sqlite3.connect(self.db_path)
            self._cursor = self._db.cursor()
            output = f(self, *args, **kwargs)
            self._db.close()
            return output
        return wrapper

    @_crud_method
    def create(self, name, text):
        query = 'INSERT INTO notes VALUES (?, ?)'
        values = (name, text)
        self._cursor.execute(query, values)
        self._db.commit()
        rowid = self._cursor.lastrowid
        return f'Note #{rowid} "{name}" created'

    @_crud_method
    def read(self, rowid):
        query = 'SELECT * FROM notes WHERE rowid=?'
        values = (rowid,)
        print(query, values)
        self._cursor.execute(query, values)
        return f'Note #{rowid}: {self._cursor.fetchone()}'

    @_crud_method
    def update(self, rowid, **kwargs):
        query = f'UPDATE notes SET ?=? WHERE rowid=?'
        values = [(k, v, rowid) for k, v in kwargs.items()]
        self._cursor.executemany(query,values)
        self._db.commit()
        return f'Note #{rowid} updated'

    @_crud_method
    def delete(self, rowid):
        query = f'DELETE FROM notes WHERE rowid=?'
        values = (rowid,)
        self._cursor.execute(query, values)
        self._db.commit()
        return f'Note #{rowid} deleted'

    def execute(self, action):
        method_to_call = getattr(self, action.name)
        return method_to_call(**action.data)
