import pdb
import redis

class RedisController:
    def __init__(self, host='localhost', port=6379, db=0):
        self.r = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def init_db(self):
        self.r.flushdb()

    def add_object(self, data):
        id = self.r.incr('id')  
        key = f'{data["model"]}:{id}'
        self.r.hmset(key, data["object"])
        data['object']['id'] = id
        for i in data['indexes']:
            key = f'{data["model"]}.{i}.index'
            self.r.zadd(key, {data["object"][i]: id})
            object
        return data

    @property
    def last_id(self):
        id = self.r.get('id')
        return id if id >= 0 else None

rc = RedisController()

