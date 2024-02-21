import os

import pytz

from src.api.middleware.custom_exceptions.JWTKeyNotSet import JWTKeyNotSet


def load_env_with_default(env_name: str, default_value):
    if env_name in os.environ:
        env_value = os.environ[env_name]
        if env_value.lower() == 'true':
            return True
        if env_value.lower() == 'false':
            return False
        return env_value
    else:
        return default_value


# Database

DATABASE_USERNAME_USER = load_env_with_default('DATABASE_USERNAME_USER', 'root')
DATABASE_PASSWORD_USER = load_env_with_default('DATABASE_PASSWORD_USER', 'not set')
DATABASE_USER = load_env_with_default('DATABASE_USER', 'fastapi_app')
DATABASE_HOST = load_env_with_default('DATABASE_HOST', 'mysql')
DATABASE_PORT_USER = load_env_with_default('DATABASE_PORT_USER', 3306)

DATABASE_USERNAME_MUSIC = load_env_with_default('DATABASE_USERNAME_MUSIC', 'root')
DATABASE_PASSWORD_MUSIC = load_env_with_default('DATABASE_PASSWORD_MUSIC', 'not set')
DATABASE_MUSIC = load_env_with_default('DATABASE_MUSIC', 'fastapi_app_music')
DATABASE_PORT_MUSIC = load_env_with_default('DATABASE_PORT_MUSIC', 3308)

RUN_IN_DOCKER_COMPOSE = load_env_with_default('RUN_IN_DOCKER_COMPOSE',
                                              False)  # env. is always as string --> no boolean without parsing

if RUN_IN_DOCKER_COMPOSE:
    SQLALCHEMY_DATABASE_URI_USER = f"{DATABASE_HOST}+pymysql://{DATABASE_USERNAME_USER}:{DATABASE_PASSWORD_USER}@host.docker.internal:{DATABASE_PORT_USER}/{DATABASE_USER}"
    SQLALCHEMY_DATABASE_URI_MUSIC = f"{DATABASE_HOST}+pymysql://{DATABASE_USERNAME_MUSIC}:{DATABASE_PASSWORD_MUSIC}@host.docker.internal:{DATABASE_PORT_MUSIC}/{DATABASE_MUSIC}"
    REQUEST_TO_ID3_SERVICE = "127.0.0.1"
else:
    SQLALCHEMY_DATABASE_URI_USER = f"{DATABASE_HOST}+pymysql://{DATABASE_USERNAME_USER}:{DATABASE_PASSWORD_USER}@localhost:{DATABASE_PORT_USER}/{DATABASE_USER}"
    SQLALCHEMY_DATABASE_URI_MUSIC = f"{DATABASE_HOST}+pymysql://{DATABASE_USERNAME_MUSIC}:{DATABASE_PASSWORD_MUSIC}@localhost:{DATABASE_PORT_MUSIC}/{DATABASE_MUSIC}"
    REQUEST_TO_ID3_SERVICE = "id3-app"  # container name of the id3-service

# JWT Token encryption/decryption

ALGORITHM = load_env_with_default('ALGORITHM', 'HS256')
TOKEN_EXPIRE_MINS = int(load_env_with_default('TOKEN_EXPIRE_MINS', 30))
REFRESH_TOKEN_EXPIRE_HOURS = int(load_env_with_default('REFRESH_TOKEN_EXPIRE_HOURS', 10))
TIMEZONE = load_env_with_default('TIMEZONE', pytz.timezone('CET'))
SECRET_KEY = load_env_with_default('SECRET_KEY', 'key not set')

if SECRET_KEY == 'key not set':
    raise JWTKeyNotSet()
    # If Private Key for JWT is not set, crash the complete service because it's a major security risk
