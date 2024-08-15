import orjson
import strawberry
from fastapi import Depends, Request
from strawberry.fastapi import BaseContext, GraphQLRouter
from strawberry.http import GraphQLHTTPResponse
from strawberry.schema.config import StrawberryConfig
from strawberry.types import ExecutionResult

from src.app.routers.graphql.schemas.query_schemas import Query
from src.app.utils.response_helper import error_response, success_response
from src.app.utils.schemas.output_schemas import ErrorSchemas


class MyGraphQLRouter(GraphQLRouter):
    async def process_result(
        self, request: Request, result: ExecutionResult
    ) -> GraphQLHTTPResponse:
        if result.errors:
            response = error_response(
                request,
                "VALIDATION_ERROR",
                details=[
                    ErrorSchemas(loc=err.path, msg=err.formatted.get("message"))
                    for err in result.errors
                ],
            )
        response = success_response(result.data, request)
        return orjson.loads(response.body)


class CustomContext(BaseContext):
    def __init__(self, greeting: str, name: str):
        self.greeting = greeting
        self.name = name


def custom_context_dependency() -> CustomContext:
    return CustomContext(greeting="you rock!", name="John Doe")


async def get_context(
    custom_context=Depends(custom_context_dependency),
):
    return custom_context


schema = strawberry.Schema(Query, config=StrawberryConfig(auto_camel_case=False))

graphql_app = MyGraphQLRouter(schema, context_getter=get_context, allow_queries_via_get=True)
