from typing import Type
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, Field, field_validator


class CircuitBreakerInputDto(BaseModel):
    half_open_retry_count: int = Field(default=3, ge=0, le=100)
    half_open_retry_timeout_seconds: int = Field(default=120, ge=30, le=1800)

    exception_list: list[Type[Exception] | type[HTTPException]] = Field(default=[Exception, HTTPException])

    @field_validator("exception_list")
    @classmethod
    def validate_exception_list(cls, v: list[Type[Exception] | type[HTTPException]]) -> list[Type[Exception] | type[HTTPException]]:
        if v is None or len(v) == 0:
            return (Exception,)

        return tuple(set(v))

    class Config:
        arbitrary_types_allowed = True