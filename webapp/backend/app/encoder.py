import json
import datetime


class ObjectEncoder(json.JSONEncoder):

    def default(self, obj):
        if hasattr(obj, 'to_json'):
            return obj.to_json()
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

        return super().default(obj)
