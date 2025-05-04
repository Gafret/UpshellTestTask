from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends, Query
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from app.backend.const import Roles
from app.backend.dependencies import check_permission, check_jwt_token
from app.backend.openapi import DevicesRouteResponses
from app.backend.session import SessionDependency
from app.models.devices import Device
from app.schemas.devices import DeviceFilterQueryParams, UserDeviceCart, DeviceCreate, DeviceFilterResult, \
    CartPurchaseResult
from app.services.devices import DeviceDataManager, DeviceService

router = APIRouter(tags=["Товары"])


@router.post("/device",
             status_code=HTTP_201_CREATED,
             name="Добавить товар в каталог",
             description="Добавление нового товара в каталог. Доступно только для администраторов",
             responses=DevicesRouteResponses.add_device_responses,
             dependencies=[Depends(check_permission(Roles.ADMIN))])
async def add_device(device_info: DeviceCreate, session: SessionDependency) -> Device:
    device_info = Device.model_validate(device_info)
    device = DeviceDataManager(session).add_device(device_info)

    return device


@router.get("/devices",
            status_code=HTTP_200_OK,
            name="Получить список доступных к продаже товаров",
            description="Возвращает список устройств, доступных для покупки",
            responses=DevicesRouteResponses.devices_responses)
async def get_device_catalog(filters: Annotated[DeviceFilterQueryParams, Query()],
                             session: SessionDependency) -> DeviceFilterResult:
    devices = DeviceService(session).get_devices(filters)

    return devices


@router.post("/buy",
             status_code=HTTP_200_OK,
             name="Покупка выбранных товаров",
             description="Эндпоинт для покупки выбранных товаров в интернет-магазине электроники. "
                         "Доступно только для авторизованных пользователей.",
             responses=DevicesRouteResponses.buy_responses,
             dependencies=[Depends(check_jwt_token)])
async def purchase_device(user_cart: UserDeviceCart, session: SessionDependency) -> CartPurchaseResult:
    purchase_result = DeviceService(session).purchase_devices(user_cart)

    return purchase_result
