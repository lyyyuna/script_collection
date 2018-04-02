class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)

        tablename = attrs.get('__table__', None) or name
        print 'Get table name', tablename
        return type.__new__(cls, name, bases, attrs)


class Model(dict):
    __metaclass__ = ModelMeta
    __table__ = 'Should not show'

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


class User(Model):
    __table__ = 'User table'


u = User()