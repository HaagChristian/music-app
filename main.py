import logging
import uuid

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from src.api.routers import registration, user, id3_service

version: str = "0.0.1"
app_name: str = "MusicApp Service"
instance_uuid: str = str(uuid.uuid4())
app_description: str = "This is a simple music app service. It provides a RESTful API to manage users and their music preferences. " \
                       "It is part of a microservice architecture and is designed to be scalable and fault-tolerant. " \
                       "It is written in Python using the FastAPI framework and uses a MySQL database to store user and music data. " \
                       "It is deployed in a Docker container."
contact_name: str = "Christian Haag"

app = FastAPI(
    title=app_name,
    description=app_description,
    version=version,
    docs_url="/api",
    contact={"name": contact_name},
)

app.include_router(registration.router)
app.include_router(user.router)
app.include_router(id3_service.router)

# CORS is required to run api simultaneously with website on local machine
# Allow localhost:8000 and 127.0.0.1:8000 to access the api
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def main():
    logging.info("run main")
    uvicorn.run(app, port=8000)


@app.get("/")
def rootreq():
    return {"home"}


@app.get("/health")
def health(request: Request):
    correlation_id = request.headers.get("X-Correlation-ID", default="not set")


if __name__ == "__main__":
    main()
