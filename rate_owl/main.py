from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def test_route() -> str:
    return "Hello world!"
