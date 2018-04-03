class Field(object):
    def __init__(self, name, sqlType, primaryKey, default):
        self.name = name
        self.sqlType = sqlType
        self.primaryKey = primaryKey
        self.default = default

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__, self.sqlType, self.name)


class StringField(Field):
    def __init__(self, name=None, sqlType='character varying(100)', primaryKey=False, default=''):
        super(StringField, self).__init__(name, sqlType, primaryKey, default)


class IntegerField(Field):
    def __init__(self, name=None, sqlType='integer', primaryKey=False, default=0):
        super(IntegerField, self).__init__(name, sqlType, primaryKey, default)