import json
import redis

r = redis.Redis(host = 'localhost', port=6379, db=0, decode_responses=True)

def update(object_type, fields_dict, id=None):
    if not id:
        r.incr('id')
        id = r.get('id')
    key = f'{object_type}:{id}'
    for field in fields_dict:
        r.hset(key, field, fields_dict[field])
    r.sadd(object_type, key)
    return {'error': 'no', 'message': '{key} updated'}

def read(object_type, id=None):
    return [dict(r.hgetall(key), id=key.lstrip(f'{object_type}:'))  for key in r.keys(f'{object_type}:{"*" if not id else id}')]

def delete(object_type, id):
    key = f'{object_type}:{id}'
    r.delete(key)
    return {'error': 'no', 'message': '{key} deleted'}


def initialize_db(initial_data = None):
    r.flushdb()
    r.set('id', -1)
    if initial_data:
        for object_type in test_data:
            for object in test_data[object_type]:
                update(object_type, object)

if __name__=='__main__': 
    from fixtures import test_data
    initialize_db()
