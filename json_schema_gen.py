#!/usr/bin/env python3
"""JSON Schema generator — infer schema from JSON data."""
import sys, json

def infer_type(value):
    if value is None: return {"type": "null"}
    if isinstance(value, bool): return {"type": "boolean"}
    if isinstance(value, int): return {"type": "integer"}
    if isinstance(value, float): return {"type": "number"}
    if isinstance(value, str): return {"type": "string"}
    if isinstance(value, list):
        if not value: return {"type": "array", "items": {}}
        items = [infer_type(v) for v in value]
        return {"type": "array", "items": items[0]}  # simplified
    if isinstance(value, dict):
        props = {k: infer_type(v) for k, v in value.items()}
        return {"type": "object", "properties": props, "required": list(value.keys())}
    return {"type": "string"}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        data = json.load(open(sys.argv[1]))
    elif not sys.stdin.isatty():
        data = json.load(sys.stdin)
    else:
        data = {"name": "test", "age": 25, "scores": [95, 87], "active": True, "address": {"city": "SF"}}
    schema = infer_type(data)
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    print(json.dumps(schema, indent=2))
