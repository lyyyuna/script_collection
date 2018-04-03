from field import *

def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)


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
        if primary == None:
            raise RuntimeError("No primary key given.")
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda x: "'%s'" % x, fields))
        # renew attrs
        attrs['__mappings__'] = mappings 
        attrs['__table__'] = tablename
        attrs['__primarykey__'] = primary 
        attrs['__fields__'] = fields 
        # some basic sql commands
        attrs['__select__'] = "select '%s', %s from '%s'" % (primary, ','.join(escaped_fields), tablename)
        attrs['__insert__'] = "insert into '%s' (%s, '%s') values (%s)" % (tablename, ','.join(escaped_fields), primary, create_args_string(len(escaped_fields)+1))
        attrs['__update__'] = "update '%s' set %s where '%s' =?" % (tablename, ','.join(map(lambda x: "'%s'=?" % (mappings.get(x).name), fields)), primary)
        attrs['__delete__'] = "delete from '%s' where '%s' = ?" % (tablename, primary)
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

    @classmethod
    def select(cls, id):
        print "%s where '%s' = %s;" % (cls.__select__, cls.__primarykey__, id)

    def getValue(self, k):
        value = getattr(self, k, None)
        if value is not None:
            field = self.__mappings__[k]
            if field.default is not None:
                value = field.default
                setattr(self, k, value)

    def save(self):
        args = map(self.getValue, self.__fields__)
        args.append(self.getValue(self.__primarykey__))
        print self.__insert__, args


class User(Model):
    __table__ = 'User_table'
    student_id = IntegerField('studentid', primaryKey=True)
    name = StringField('username')
    age = IntegerField('age')


print 'Test relation fields Auto Finding:'
u = User()
print

print 'Test select sql command:'
User.select(id=1)
print

print 'Test insert sql command:'
u2 = User(student_id=3, name='blue', age=123)
u2.save()