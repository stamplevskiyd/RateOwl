from fastapi import FastAPI

from owl_core.api.router import api_router

app = FastAPI()

app.include_router(api_router)


@app.get("/")
async def test_route() -> str:
    return "Hoot!"
