from fastapi import FastAPI

app = FastAPI()


@app.get("/test-failure-endpoint")
def test_failure_endpoint():
    pass


if __name__ == "__main__":
    pass
