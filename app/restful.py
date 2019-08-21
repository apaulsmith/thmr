import datetime
import enum
import json
import re
import uuid


def all_as_dict(iterable):
    result = {}
    for i in iterable:
        d = one_as_dict(i)
        result[i.id] = d

    return result


def all_as_list(iterable):
    result = []
    for i in iterable:
        d = one_as_dict(i)
        result.append(d)

    return result


def one_as_dict(item):
    return item.as_dict()


def json_dumps(data):
    return json.dumps(data, cls=CustomJSONEncoder)


def json_loads(s):
    return json.loads(s, cls=CustomJSONDecoder)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        elif isinstance(obj, enum.Enum):
            return str(obj)

        return json.JSONEncoder.default(self, obj)


class CustomJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
        self.enum_regex = re.compile(r"^([a-zA-Z]+)\.([a-zA-Z]+)$")

    def object_hook(self, source):
        for k, v in source.items():
            if isinstance(v, str):
                try:
                    d = datetime.datetime.fromisoformat(str(v))
                    if d.hour == 0 and d.minute == 0 and d.second == 0 and d.microsecond == 0:
                        d = datetime.date(d.year, d.month, d.day)
                    source[k] = d

                    continue
                except:
                    pass

                try:
                    source[k] = self.parse_enum(str(v))
                    continue
                except:
                    pass

        return source

    def parse_enum(self, v):
        match = self.enum_regex.match(v)
        if match:
            enum_name = match.group(1)
            enum_value = match.group(2)

            e = schema.KNOWN_ENUMS.get(enum_name)
            if e:
                return e[enum_value]

        raise ValueError('{} is not a known enum value!'.format(v))
