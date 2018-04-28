class ModelType(type):
    def __new__(cls, name, bases, attrs):
        tablename = attrs.get('__table__', None) or name
        print 'Get table name', tablename
        return type.__new__(cls, name, bases, attrs)

class Model(dict):
    __metaclass__ = ModelType

class User(Model):
    __table__ = 'User_table'
