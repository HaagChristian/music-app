import logging
import uuid

import uvicorn
from fastapi import FastAPI
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.api.middleware.authjwt import AuthJwt
from src.api.middleware.custom_exceptions.unauthorized import Unauthorized
from src.api.routers import registration, user, id3_service, search, encoder_service, crud
from src.settings.error_messages import MISSING_TOKEN

version: str = "0.0.1"
app_name: str = "MusicApp Service"
instance_uuid: str = str(uuid.uuid4())
app_description: str = "This is a simple music app service. " \
                       "It provides a RESTful API to manage users and their music preferences. " \
                       "It is part of a microservice architecture and is designed to be scalable and fault-tolerant. " \
                       "It is written in Python using the FastAPI framework and uses a MySQL database" \
                       " to store user and music data. "

contact_name: str = "Selina Weh / Christian Haag"

http_bearer = HTTPBearer()

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
app.include_router(search.router)
app.include_router(encoder_service.router)
app.include_router(crud.router)

# CORS is required to run api simultaneously with website on local machine
# Allow localhost:8000 and 127.0.0.1:8000 to access the api

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://localhost:4200",
    "http://127.0.0.1"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


def auth_validate(request: Request):
    if '/id3service' in request.url.path or 'user/me' in request.url.path or '/data/search' in request.url.path or \
            '/data/change-metadata' in request.url.path or '/encoderservice' in request.url.path:
        try:
            # create HTTPAuthorizationCredentials for better token handling
            token_str = request.headers.get("authorization", None)
            if token_str is None:
                raise Unauthorized(MISSING_TOKEN)
            prefix, token = token_str.split(" ", 1)
            token = HTTPAuthorizationCredentials(scheme=prefix, credentials=token)

            auth = AuthJwt()
            auth.decode_token(jwt_token=token)
            # add user_email to request state
            email_from_jwt = auth.get_token_data_from_decoded_token
            request.state.user_email = email_from_jwt
        except Unauthorized:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object


@app.middleware("http")
async def middleware_auth_check(request: Request, call_next):
    """ Middleware to check if the user has a valid jwt token to access the endpoints """
    # if request.scope.method is OPTIONS, the request is a preflight (CORS) request
    if request.scope.get('method') != "OPTIONS":
        res = auth_validate(request)

        if res is not None:
            return JSONResponse(status_code=401, content=res)
    response = await call_next(request)
    return response


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
