class Model(dict):
    def __new__(cls, name, bases, attrs):
        tablename = attrs.get('__table__', None) or name
        print ('Get table name', tablename)
        return type.__new__(cls, name, bases, attrs)


class User(Model):
    __table__ = 'User_table'


u1 = User(3, 4, 5)