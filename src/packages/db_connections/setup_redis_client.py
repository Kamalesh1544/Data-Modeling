from redis import asyncio as redis

from src.packages.db_connections.abstract_connection import RedisClientAbstract


class RedisClient(RedisClientAbstract):
    def __init__(self):
        self.client = None

    async def initialize_redis(self, url):
        if not url:
            raise ValueError("Redis URL not provided. Please provide a valid Redis URL.")
        if not self.client:
            connection = redis.ConnectionPool.from_url(url)
            self.client = redis.Redis.from_pool(connection)

    async def close(self):
        if self.client:
            await self.client.aclose()

    async def get_client(self):
        if not self.client:
            raise ValueError(
                "Redis client not initialized. Please ensure initialize_redis is called first."
            )
        return self.client

    async def clear_redis(self):
        if not self.client:
            raise ValueError(
                "Redis client not initialized. Please ensure initialize_redis is called first."
            )
        await self.client.flushall(asynchronous=True)


class InMemoryRedisClient(RedisClientAbstract):
    def __init__(self) -> None:
        self.data: dict = {}
        self.initialized: bool = False

    async def initialize_redis(self, url) -> None:
        self.initialized = True

    async def close(self) -> None:
        self.data.clear()
        self.initialized = False

    async def get_client(self):
        if not self.initialized:
            raise ValueError(""""In-memory client not initialized.
                             Please ensure initialize_redis is called first.""")
        return self

    async def clear_redis(self):
        if not self.initialized:
            raise ValueError("""In-memory client not initialized.
                                Please ensure initialize_redis is called first.""")
        self.data.clear()

    async def set(self, key, value):
        self.data[key] = value
        return True

    async def get(self, key):
        return self.data.get(key)

    async def delete(self, key):
        if key in self.data:
            del self.data[key]
            return True
        return False

    async def flushall(self, asynchronous=False):
        self.data.clear()
