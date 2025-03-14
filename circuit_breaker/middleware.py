from fastapi import Request
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware

from .schemas import CircuitBreakerInputDto
from .circuit_breaker import CircuitBreaker


class CircuitBreakerMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, app, circuit_breaker_input: CircuitBreakerInputDto | None = None
    ):
        super().__init__(app)
        if circuit_breaker_input is None:
            circuit_breaker_input = CircuitBreakerInputDto()

        self.circuit_breaker = CircuitBreaker(
            circuit_breaker_input=circuit_breaker_input
        )

    async def dispatch(self, request: Request, call_next: Callable):
        await self.circuit_breaker.handle_circuit_breaker(
            func=call_next,
            request=request,
        )
