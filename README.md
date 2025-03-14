# Circuit Breaker Pattern in Python

## Overview
The **Circuit Breaker** pattern is a design pattern used to improve system resilience by preventing continuous failures in a system. It acts as a safeguard by **monitoring requests** and stopping repeated failures from affecting performance.

## How It Works
1. **Closed State**: The system operates normally and allows requests.
2. **Open State**: If failures exceed a threshold, the circuit "opens," stopping further requests for a cooldown period.
3. **Half-Open State**: After a cooldown, a few test requests are allowed. If they succeed, the circuit closes; otherwise, it stays open.

## Why Use Circuit Breaker?
- Prevents cascading failures in distributed systems.
- Improves system reliability and recovery.
- Reduces unnecessary load on failing services.

## Example Usage in Python
```python
import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from circuit_breaker import CircuitBreakerMiddleware, CircuitBreakerInputDto

app = FastAPI()


@app.get("/success-endpoint")
async def success_endpoint():
    return "success"


@app.get("/failure-endpoint")
async def faulty_endpoint():
    raise HTTPException(status_code=500)


app.add_middleware(
    CircuitBreakerMiddleware,
    circuit_breaker_input=CircuitBreakerInputDto(
        exception_list=(Exception,),
        half_open_retry_count=3,
        half_open_retry_timeout_seconds=30,
    ),
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```
