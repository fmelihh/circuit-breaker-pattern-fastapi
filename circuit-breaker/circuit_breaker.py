from typing import Generator
from contextlib import asynccontextmanager

from .schemas import CircuitBreakerInputDto


class CircuitBreaker:
    def __init__(self, circuit_breaker_input: CircuitBreakerInputDto | None = None):
        if circuit_breaker_input is None:
            circuit_breaker_input = CircuitBreakerInputDto()

        self.circuit_breaker_input = circuit_breaker_input

    @asynccontextmanager
    def handle_circuit_breaker(self) -> Generator[None, None, None]:
        try:
            pass
        except self.circuit_breaker_input.exception_list as e:
            pass
