from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBearer
from sqlalchemy.exc import NoResultFound
from starlette import status

from src.api.middleware.custom_exceptions.unauthorized import Unauthorized
from src.api.middleware.exceptions import exception_mapping
from src.api.myapi.user_model import UserResponseModel
from src.database.db import get_db
from src.service.login.user_data import get_current_user

http_bearer = HTTPBearer()
router = APIRouter(
    prefix="/api/user", tags=["Get User Data"], dependencies=[Depends(http_bearer)]
)


@router.get("/me", response_model=UserResponseModel)
def read_users_me(request: Request, db=Depends(get_db)):
    try:
        return get_current_user(jwt_payload=request.state.user_email, db=db)
    except (Unauthorized, NoResultFound) as e:
        http_status, detail_function = exception_mapping.get(type(e), (
            status.HTTP_500_INTERNAL_SERVER_ERROR, lambda e: str(e.args[0])))
        raise HTTPException(status_code=http_status, detail=detail_function(e))
