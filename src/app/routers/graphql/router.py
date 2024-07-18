import strawberry
from fastapi import Depends
from strawberry.fastapi import BaseContext, GraphQLRouter

from src.app.routers.graphql.schemas.query_schemas import Query


class CustomContext(BaseContext):
    def __init__(self, greeting: str, name: str):
        self.greeting = greeting
        self.name = name


def custom_context_dependency() -> CustomContext:
    return CustomContext(greeting="you rock!", name="John")


async def get_context(
    custom_context=Depends(custom_context_dependency),
):
    return custom_context


schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,
)
