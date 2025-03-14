from pydantic import BaseModel, Field, field_validator


class CircuitBreakerInputDto(BaseModel):
    half_open_retry_count: int = Field(default=3, ge=0, le=100)
    half_open_retry_timeout_seconds = Field(default=120, ge=30, le=1800)

    exception_list: tuple[Exception] | None = Field(default=None)

    @field_validator("exception_list")
    @classmethod
    def validate_exception_list(cls, v: tuple[Exception] | None) -> tuple[Exception]:
        if v is None or len(v) == 0:
            return (Exception,)

        return tuple(set(v))
