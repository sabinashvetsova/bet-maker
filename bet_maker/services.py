from aioredis import Redis


class Service:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def set_value(self, key, values):
        await self._redis.hset(key, mapping=values)

    async def add_index(self, name, values):
        await self._redis.sadd(name, values)

    async def get_hash_values(self, key) -> list:
        cur = b'0'
        data = []
        keys = []
        while cur:
            cur, keys = await self._redis.scan(cur, match=key, count=1000000)
        for key in keys:
            values = await self._redis.hgetall(key)
            data.append(values)
        return data

    async def get_set_values(self, name) -> list:
        cur = b'0'
        keys = []
        while cur:
            cur, keys = await self._redis.sscan(name, cur, count=1000000)
        return keys

    async def change_field_value(self, keys, values_to_change):
        for key in keys:
            values = await self._redis.hgetall(key)
            values.update(values_to_change)
            await self._redis.hset(key, mapping=values)
