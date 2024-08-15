from typing import Any

from neo4j import GraphDatabase
from tortoise.connection import connections

from src.app.core.config.settings import get_settings


class PostgresDatabaseConnection:
    """Connects to the PostgreSQL database.

    Args:
        database_url (str): The URL of the PostgreSQL database.
    Returns:
        PostgresDatabaseConnection: An instance of the PostgresDatabaseConnection class.
    """

    async def execute_query(self, query: str, parameters: list[Any]):
        con = connections.get("default")
        return await con.execute_query(query, parameters)


class GraphDatabaseConnection:
    """Connects to the Neo4j graph database.

    Args:
        graph_url (str): The URL of the Neo4j graph database.
        graph_user (str): The username for the Neo4j graph database.
        graph_password (str): The password for the Neo4j graph database.

    Returns:
        GraphDatabaseConnection: An instance of the GraphDatabaseConnection class.

    """

    def __init__(
        self,
        graph_url: str = get_settings().GRAPH_URL,
        graph_user: str = get_settings().GRAPH_USER,
        graph_password: str = get_settings().GRAPH_PASSWORD,
    ):
        self.driver = GraphDatabase.driver(graph_url, auth=(graph_user, graph_password))
        self.session = self.driver.session()

    async def close(self):
        await self.session.close()
        await self.driver.close()
