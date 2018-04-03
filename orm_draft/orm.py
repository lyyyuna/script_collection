from field import *


class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)

        tablename = attrs.get('__table__', None) or name
        print 'Get table name', tablename
        mappings = {}
        fields = []
        primary = None
        for k, v in attrs.iteritems():
            if isinstance(v, Field):
                print 'Found one field', k
                mappings[k] = v
                if v.primaryKey == True:
                    if primary == None:
                        primary = k
                    else:
                        raise RuntimeError("Duplicate primary key: %s", k)
                else:
                    fields.append(k)
        for k in mappings.keys():
            attrs.pop(k)
        # renew attrs
        attrs['__mappings__'] = mappings 
        attrs['__table__'] = tablename
        attrs['__primary_key__'] = primary 
        attrs['__fields__'] = fields 
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
    name = StringField('username', primaryKey=True)
    age = IntegerField('age')


u = User()