from fastapi.exceptions import HTTPException


class CircuitBreakerRemoteCallException(HTTPException):
    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = (
                "The system is experiencing high failure rates. Please try again later."
            )

        super().__init__(status_code=503, detail=message)


__all__ = ["CircuitBreakerRemoteCallException"]
