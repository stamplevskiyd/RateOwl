from fastapi import FastAPI

from owl_core.api.router import api_router
from owl_core.views.router import views_router
from fastapi.middleware.cors import CORSMiddleware

from owl_core.middlewares import SetUserMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SetUserMiddleware)


app.include_router(api_router)
app.include_router(views_router)


@app.get("/ping")
async def test_route() -> str:
    return "Hoot!"
