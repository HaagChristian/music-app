# FastAPI Music Web-Service

## Description

### Authentication

This API provides endpoints for:

- user registration (create account)
- user login (create access and refresh token)
- refresh token (create new access token based on refresh token)
- ge user info (get user info from logged in user)

### Music

The main purpose of this API is to provide endpoints for working with music files.
Therefore, this API uses the ID3 and Encoder Services.

The Music Services provides endpoints for:

- uploading music files (mp3 files | using the ID3 Service)
- change metadata in the database and for the corresponding music file (using the ID3 Service)

## Installation

**_NOTE:_** Use a virtual environment to install the required packages.

It is possible to run the service as standalone or in a docker container. If you want to run the service as standalone,
it is necessary to install the required packages based on your operating system. Furthermore, its necessary to start the
ID3 and Encoder Services.

Run on Linux:

```bash

pip install -r requirements_for_linux.txt

```

Run on Windows:

```bash

pip install -r requirements_for_windows.txt

```

After startup the Music Service is available on `http://127.0.0.1:8000/api'

## Error handling

The application handles all known exceptions and raises errors to the user in a user-friendly manner.
This includes the underlying services (ID3 and Encoder).

### Unhandled Exceptions

It is possible that some exceptions are thrown without any error handling. This is due to the fact that these errors
should be tracked with an error tracking tool (e.g. Sentry).
This would allow the developers to identify and fix the errors.

Examples for these errors are:

- Connection errors
    - Database connection
    - Service connection
- Missing environment variables

### Error messages

The errors thrown by the application should not indicate the original problem. Therefore, the errors were intercepted
and replaced by general error messages. This improves security, as it prevents the user from drawing conclusions about
existing data.

## Environment Variables

All required envs are saved in the local.env file
The following environment variables are required:

### General database

- DATABASE_HOST

### User database

- DATABASE_USER
- DATABASE_PASSWORD_USER
- DATABASE_PORT_USER
- DATABASE_USERNAME_USER

### Music database

- DATABASE_MUSIC
- DATABASE_PASSWORD_MUSIC
- DATABASE_PORT_MUSIC
- DATABASE_USERNAME_MUSIC

### Authentication

- ALGORITHM
- TOKEN_EXPIRE_MINS
- REFRESH_TOKEN_EXPIRE_HOURS
- SECRET_KEY

### Standalone or Docker

- RUN_IN_DOCKER_COMPOSE
