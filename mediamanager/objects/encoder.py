import json
import datetime

class ObjectEncoder(json.JSONEncoder):

    def default(self, obj):
        from mediamanager.objects.video import Entry
        if isinstance(obj, Entry):
            return obj.to_json()
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

        return super().default(obj)
