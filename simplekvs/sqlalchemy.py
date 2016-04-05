import os
from sqlalchemy import create_engine, MetaData, Table, Column, String, Text, event
from sqlalchemy.sql import select
from .store import Store


class SQLAlchemyStore(Store):
    """
    A key-value store backed by a SQLAlchemy connection.
    """
        
    def __init__(self, storepath):
        engine = create_engine("sqlite:///%s" % storepath, echo=False)
        
        @event.listens_for(engine, "connect")
        def _on_connect(dbapi_connection, connection_record):
            # disable pysqlite's emitting of the BEGIN statement entirely.
            # also stops it from emitting COMMIT before any DDL.
            dbapi_connection.isolation_level = None
            dbapi_connection.execute('PRAGMA journal_mode = WAL')
        
        @event.listens_for(engine, "begin")
        def _on_begin(conn):
            # emit our own BEGIN
            conn.execute("BEGIN IMMEDIATE")
        
        metadata = MetaData()
        kvs_table = Table('kvs', metadata,
            Column('key', String(255), primary_key=True),
            Column('value', Text)
        )
        metadata.create_all(engine)
        
        self.db = engine.connect()
        self.table = kvs_table
    
    def __enter__(self):
        return self
    
    def __exit__(self, rtype, rvalue, rtraceback):
        pass
    
    def set(self, key, value):
        # First, try an insert.
        t = self.db.begin()
        try:
            ins = self.table.insert()
            res = self.db.execute(ins, key=key, value=value)
            t.commit()
            
            # On success, return
            return
            
        except:
            t.rollback()
            return
        
        # We only get here on failure to insert, so try an update.
        t = self.db.begin()
        try:
            upd = self.table.update().where(self.table.c.key==key).values(value=value)
            self.db.execute(upd)
            t.commit()
            return
        except:
            t.rollback()
            raise

    def get(self, key):
        s = select([self.table.c.value]).where(self.table.c.key==key)
        res = self.db.execute(s)
        value = res.fetchone()
        if value:
            return value[0]
        else:
            raise KeyError(key)

    def delete(self, key):
        t = self.db.begin()
        try:
            s = self.table.delete().where(self.table.c.key==key)
            self.db.execute(s)
            t.commit()
            return
        
        except:
            t.rollback()
            raise

    def keys(self):
        s = select([self.table.c.key])
        res = self.db.execute(s)
        result = res.fetchall()
        result = [x[0] for x in result]  # unpack from per-row
        return result

    def values(self):
        s = select([self.table.c.value])
        res = self.db.execute(s)
        result = res.fetchall()
        result = [x[0] for x in result]  # unpack from per-row
        return result
