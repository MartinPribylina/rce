import json


class JsonSerializer:
    def serialize(self, obj) -> str:
        return json.dumps(obj, default=self.custom_serializer)
    
    def custom_serializer(self, obj):
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

