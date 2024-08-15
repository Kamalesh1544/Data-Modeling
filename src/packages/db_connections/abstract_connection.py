from abc import ABC, abstractmethod


class RedisClientAbstract(ABC):
    @abstractmethod
    async def initialize_redis(self, url):
        pass

    @abstractmethod
    async def close(self):
        pass

    @abstractmethod
    async def get_client(self):
        pass

    @abstractmethod
    async def clear_redis(self):
        pass
