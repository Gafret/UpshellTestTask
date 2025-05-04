from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends, Query
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, \
    HTTP_200_OK

from app.backend.const import Roles
from app.backend.dependencies import check_permission, check_jwt_token
from app.backend.session import SessionDependency
from app.models.devices import Device
from app.schemas.devices import DeviceFilterQueryParams, UserDeviceCart, DeviceCreate, DeviceFilterResult, \
    CartPurchaseResult
from app.services.devices import DeviceDataManager, DeviceService

router = APIRouter(tags=["devices"])


@router.post("/device",
             status_code=HTTP_201_CREATED,
             description="Дает пользователю с ролью админа добавить устройство",
             responses={
                 HTTP_400_BAD_REQUEST: {"description": "Отправленная информация не прошла валидацию"},
                 HTTP_201_CREATED: {"description": "Девайс добавлен в каталог"},
                 HTTP_401_UNAUTHORIZED: {"description": "Неавторизованный запрос"},
                 HTTP_403_FORBIDDEN: {"description": "Недостаточно прав"},
             },
             dependencies=[Depends(check_permission(Roles.ADMIN))])
async def add_device(device_info: DeviceCreate, session: SessionDependency) -> Device:
    device_info = Device.model_validate(device_info)
    device = DeviceDataManager(session).add_device(device_info)

    return device


@router.get("/devices",
            status_code=HTTP_200_OK,
            description="Позволяет получить все девайсы по определенным параметрам фильтрования",
            responses={
                 HTTP_400_BAD_REQUEST: {"description": "Ошибка в параметрах фильтрации"},
                 HTTP_200_OK: {"description": "Получен список фильтрованных девайсов"},
            })
async def get_device_catalog(filters: Annotated[DeviceFilterQueryParams, Query()],
                             session: SessionDependency) -> DeviceFilterResult:
    devices = DeviceService(session).get_devices(filters)

    return devices


@router.post("/buy",
             status_code=HTTP_200_OK,
             description="Оформляет покупку корзины пользователя",
             responses={
                 HTTP_400_BAD_REQUEST: {"description": "Ошибка в составлении корзины"},
                 HTTP_200_OK: {"description": "Покупка прошла успешно"},
                 HTTP_401_UNAUTHORIZED: {"description": "Неавторизованный пользователь"},
             },
             dependencies=[Depends(check_jwt_token)])
async def purchase_device(user_cart: UserDeviceCart, session: SessionDependency) -> CartPurchaseResult:
    purchase_result = DeviceService(session).purchase_devices(user_cart)

    return purchase_result
