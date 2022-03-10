from typing import Any, TypeVar, Union

from pydantic import BaseModel, Field, root_validator

DataT = TypeVar("DataT")


class BodySchema(BaseModel):
    __root__: dict[Any, Any] = Field(..., example={"foo": "bar"})

    @root_validator
    def validate_body(cls, values: dict[Any, Any]) -> dict[Any, Any]:
        request_values = values["__root__"]
        error = ValueError("wrong request body")

        if not request_values:
            raise error

        if len(request_values) == 1:
            ((key, value),) = request_values.items()
            if key == "" and value == "":
                raise error

        return request_values


class SavedBodyResponse(BaseModel):
    key: str = Field(..., example="foo")


class GetBodyResponse(BaseModel):
    __root__: dict[Any, Any] = Field(..., example={"foo": "bar"})

    @root_validator
    def validate_response(cls, values: dict[Any, Any]) -> dict[Any, Any]:
        request_values = values["__root__"]
        if "duplicates" not in request_values:
            request_values["duplicates"] = 1
        return request_values

    class Config:
        schema_extra = {
            "example": {
                "foo": "bar",
                "duplicates": 1,
            },
        }


class DuplicatesBodiesResponse(BaseModel):
    percent_duplicates: Union[float, int] = Field(..., example=25)
