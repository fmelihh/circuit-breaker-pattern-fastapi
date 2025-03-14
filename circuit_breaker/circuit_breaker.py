import traceback
import pendulum as pe
from typing import Callable
from fastapi import Response
from fastapi.responses import StreamingResponse

from .enums import State
from .schemas import CircuitBreakerInputDto
from .exceptions import CircuitBreakerRemoteCallException


class CircuitBreaker:
    def __init__(self, circuit_breaker_input: CircuitBreakerInputDto | None = None):
        if circuit_breaker_input is None:
            circuit_breaker_input = CircuitBreakerInputDto()

        self._state = None
        self._failed_count = 0
        self._last_attempt_datetime = None
        self.circuit_breaker_input = circuit_breaker_input

    @property
    def state(self) -> State:
        if self._state is None:
            self._state = State.CLOSED

        return self._state

    @state.setter
    def state(self, state: State):
        self._state = state

    def _check_http_exception(self, response: StreamingResponse):
        if response.status_code < 400:
            return

        raise CircuitBreakerRemoteCallException(
            "Request failed with status code: " + str(response.status_code)
        )

    def update_last_attempt_datetime(self):
        self._last_attempt_datetime = pe.now()

    async def handle_open_state(self, func: Callable, *args, **kwargs) -> Response:
        exception_list = tuple(self.circuit_breaker_input.exception_list)

        current_datetime = pe.now()
        threshold_datetime = self._last_attempt_datetime.add(
            seconds=self.circuit_breaker_input.half_open_retry_timeout_seconds
        )
        if threshold_datetime >= current_datetime:
            raise CircuitBreakerRemoteCallException(
                message=f"Retry after {(threshold_datetime - current_datetime).seconds} secs"
            )

        self.state = State.HALF_OPEN
        try:
            response = await func(*args, **kwargs)
            self._check_http_exception(response)
            self.state = State.CLOSED
            self._failed_count = 0
            self.update_last_attempt_datetime()
            return response
        except exception_list as e:
            self._failed_count += 1
            self.update_last_attempt_datetime()
            self.state = State.OPEN

            traceback.print_exception(e)
            raise CircuitBreakerRemoteCallException

    async def handle_closed_state(self, func: Callable, *args, **kwargs) -> Response:
        exception_list = tuple(self.circuit_breaker_input.exception_list)
        try:
            response = await func(*args, **kwargs)
            self._check_http_exception(response)
            self.update_last_attempt_datetime()
            return response
        except exception_list as e:
            self._failed_count += 1
            self.update_last_attempt_datetime()

            if self._failed_count >= self.circuit_breaker_input.half_open_retry_count:
                self.state = State.OPEN

            traceback.print_exception(e)
            raise CircuitBreakerRemoteCallException

    async def handle_circuit_breaker(self, func: Callable, *args, **kwargs) -> Response:
        match self.state:
            case State.OPEN:
                response = await self.handle_open_state(func, *args, **kwargs)
            case State.CLOSED:
                response = await self.handle_closed_state(func, *args, **kwargs)
            case _:
                raise NotImplementedError("Different state strategy provided")

        return response
