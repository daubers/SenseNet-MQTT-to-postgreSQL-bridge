from sqlalchemy.ext.declarative import DeclarativeMeta
import datetime
import json


def to_dict(obj):
    if isinstance(obj.__class__, DeclarativeMeta):
        # an SQLAlchemy class
        fields = {}
        for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
            data = obj.__getattribute__(field)
            try:
                if type(data)!=datetime.datetime:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                else:
                    json.dumps(data.isoformat())
                    fields[field] = data.isoformat()
            except TypeError:
                fields[field] = None
        # a json-encodable dict
        return fields

