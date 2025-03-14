from fastapi import Request
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware

from .schemas import CircuitBreakerInputDto
from .circuit_breaker import CircuitBreaker


class CircuitBreakerMiddleware(CircuitBreaker, BaseHTTPMiddleware):
    def __init__(
        self, app, circuit_breaker_input: CircuitBreakerInputDto | None = None
    ):
        BaseHTTPMiddleware.__init__(self, app)
        CircuitBreaker.__init__(self, circuit_breaker_input)

    async def dispatch(self, request: Request, call_next: Callable):
        response = await self.handle_circuit_breaker(
            func=call_next,
            request=request,
        )

        return response
