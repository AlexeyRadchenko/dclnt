"""
SELECT name FROM sqlite_master WHERE type='table' AND name='table_name';
"""
import sqlite3


class Base:
    __tablename__ = None
    __columns__ = []
    __connection__ = None
    __cursor__ = None
    __field_names__ = None

    def __init__(self, connection, **kwargs):
        self.__connection__ = connection
        self.__cursor__ = connection.cursor()
        self.kwargs = kwargs
        self.__field_names__ = [k for k in self.__class__.__dict__.keys() if not k.startswith('__')]
        for arg in self.__field_names__:
                self.__columns__.append('%s %s' % (arg, ' '.join(self.__getattribute__(arg))))
        self.create_table()

    def __table_exist__(self):
        self.__cursor__.execute('SELECT name FROM sqlite_master WHERE type = "table" AND name = ?', (self.__tablename__,))
        tables_list = [table[0] for table in self.__cursor__.fetchall()]
        return self.__tablename__ in tables_list

    def create_table(self):
        if not self.__table_exist__():
            self.__cursor__.execute('CREATE TABLE ? (?)', (self.__tablename__, ', '.join(self.__columns__),))
        if self.kwargs:
            self.insert()

    def delete_table(self):
        if self.__table_exist__():
            self.__cursor__.execute('DROP TABLE ?', (self.__tablename__,))
            self.__connection__.commit()
            self.__connection__.close()

    def select(self):
        if not self.kwargs:
            self.__cursor__.execute('SELECT * FROM ?', (self.__tablename__,))
        else:
            self.__cursor__.execute('SELECT ? FROM ?', (
                ', '.join(self.kwargs.keys()),
                self.__tablename__,
            ))

    def insert(self):
        for key in self.kwargs.keys():
            self.__cursor__.execute('INSERT INTO "?" (""?) VALUE (?)', (self.__tablename__, key, self.kwargs[key],))
        self.__connection__.commit()
class User(Base):
    __tablename__ = 'post'
    id = ('int', 'required')
    username = ('char(256)',)

#print(User(connection=sqlite3.connect('TestDB'), id=3, username='John'))
connect = sqlite3.connect('TestDB')
user = User(connection=connect, id=1, username='John')
print(user)
#user.__delete_table__()
#User(connection=connect)
#user = User(connection=connect)

