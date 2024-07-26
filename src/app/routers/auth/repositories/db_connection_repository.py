from abc import ABC, abstractmethod

from tortoise.connection import connections


class DatabaseConnection(ABC):
    @abstractmethod
    async def execute_query(self, query: str, parameters: list):
        pass


class PostgresConnection(DatabaseConnection):
    async def execute_query(self, query: str, parameters: list):
        con = connections.get("default")
        return await con.execute_query(query, parameters)
