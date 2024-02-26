from sqlalchemy.exc import NoResultFound
from starlette import status

from src.api.middleware.custom_exceptions.MissingTitleFromMetadataError import MissingTitleFromMetadataError
from src.api.middleware.custom_exceptions.NoMetadataPassedError import NoMetadataPassedError
from src.api.middleware.custom_exceptions.WrongFileType import WrongFileType
from src.api.middleware.custom_exceptions.unauthorized import Unauthorized
from src.api.middleware.custom_exceptions.user_already_exist import UserAlreadyExistException

exception_mapping = {
    NoResultFound: (status.HTTP_404_NOT_FOUND, lambda e: str(e.args[0])),
    UserAlreadyExistException: (status.HTTP_409_CONFLICT, lambda e: str(e.args[0])),
    Unauthorized: (status.HTTP_401_UNAUTHORIZED, lambda e: str(e.args[0])),
    WrongFileType: (status.HTTP_422_UNPROCESSABLE_ENTITY, lambda e: str(e.args[0])),
    NoMetadataPassedError: (status.HTTP_422_UNPROCESSABLE_ENTITY, lambda e: str(e.args[0])),
    MissingTitleFromMetadataError: (status.HTTP_422_UNPROCESSABLE_ENTITY, lambda e: str(e.args[0]))
}
