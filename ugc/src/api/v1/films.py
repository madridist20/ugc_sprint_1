import uuid

from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import JWTDecodeError, MissingTokenError

from src.services.films import EventService, get_event_service
from src.core.config import settings
from src.models.event import EventBody, EventResponse

router = APIRouter()


@router.post('/{film_id}/event',
             response_model=EventResponse,
             description='''
             Асинхронная запись ивента в Kafka
             '''
             )
async def event_handler(
        film_id: uuid.UUID,
        body: EventBody,
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer(bearerFormat='Bearer')),
        authorize: AuthJWT = Depends(),
        event_service: EventService = Depends(get_event_service)
    ):
    """
    Записывает временную метку unix timestamp, на которой сейчас находится пользователь при просмотре фильма.
    """
    try:
        authorize.jwt_required()
    except JWTDecodeError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                            detail='Token not valid or expired')
    except MissingTokenError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                            detail='Token not found')
    token = authorize.get_raw_jwt()

    await event_service.send_event(
        topic=settings.kafka_topic,
        value=bytearray(str(body.event_time), 'utf-8'),
        key=bytearray(token['user_uuid'] + "+" + str(film_id), 'utf-8'),
    )

    return EventResponse(msg='Event time successfully sent')
