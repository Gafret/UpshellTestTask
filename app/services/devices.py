from fastapi import HTTPException
from sqlalchemy import func
from sqlmodel import select, and_
from starlette.status import HTTP_400_BAD_REQUEST

from app.models.devices import Device
from app.schemas.devices import DeviceFilterQueryParams, DeviceFilterResult, UserDeviceCart, CartPurchaseResult, \
    FulfilledDeviceOrder
from app.services.base import BaseDataManager, BaseService


class DeviceService(BaseService):
    """Сервис методов работы с девайсами в магазине"""

    def get_devices(self, filters: DeviceFilterQueryParams) -> DeviceFilterResult:
        """Получает отфильтрованные девайсы"""

        devices = DeviceDataManager(self.session).filter_devices(filters)
        result = DeviceFilterResult(items=devices, total=len(devices))

        return result

    def purchase_devices(self, purchase_order: UserDeviceCart) -> CartPurchaseResult:
        """Оформляет покупку корзины"""

        if len(purchase_order.items) == 0:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Корзина покупок пустая")

        repo = DeviceDataManager(self.session)

        total_price = 0
        filled_order = CartPurchaseResult()

        for item in purchase_order.items:
            device = Device.model_validate(item)
            db_device = repo.get_device(device)

            if db_device is None:
                raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Товар недоступен для покупки")

            if repo.get_device_count(device) < item.quantity:
                raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Недостаточно товара на складе")

            if db_device.price != item.price:
                raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                                    detail="Цена товара изменилась с момента добавления в корзину")

            sub_total = item.price * item.quantity
            cart_position = FulfilledDeviceOrder(**item.model_dump(), total_price=sub_total)
            filled_order.purchased_items.append(cart_position)

            total_price += sub_total

        filled_order.total_purchase_price = total_price

        return filled_order


class DeviceDataManager(BaseDataManager):
    """Репозиторий девайсов"""

    def add_device(self, device: Device) -> Device:
        self.add_one(device)
        self.session.commit()
        self.session.refresh(device)

        return device

    def get_device(self, device: Device) -> Device | None:
        query = (select(Device)
                 .where(and_(Device.name == device.name, Device.brand == device.brand)).limit(1))

        model = self.get_one(query)
        if not model:
            return None

        device = Device(**model.model_dump())
        return device

    def get_device_count(self, device: Device) -> int:
        query = (select(func.count(Device.id))
                 .where(and_(Device.name == device.name, Device.brand == device.brand)))
        count = self.get_one(query)

        return count

    def filter_devices(self, filter_params: DeviceFilterQueryParams) -> list[Device] | None:
        query = select(Device)
        offset = (filter_params.page - 1) * filter_params.page_size

        if filter_params.brand is not None:
            query = query.where(Device.brand == filter_params.brand)
        if filter_params.price_min is not None:
            query = query.where(Device.price >= filter_params.price_min)
        if filter_params.price_max is not None:
            query = query.where(Device.price <= filter_params.price_max)
        if filter_params.page is not None:
            query = query.offset(offset)

        query = query.limit(filter_params.page_size)

        models = self.get_all(query).all()

        if models is None:
            return None

        if offset > len(models):
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Такой страницы не существует")

        results = []
        for model in models:
            results.append(Device(**model.model_dump()))
        return results
