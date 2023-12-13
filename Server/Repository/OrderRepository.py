from sqlalchemy.orm import Session
from sqlalchemy import func, select
from ..Models import BaseOrder
from ..database import Order, Service, Client, OrderToService, StateOrder


class OrderRepository:
    def __init__(self, session: Session):
        self.__session: Session = session

    def get(self, id_order: int) -> Order:
        return self.__session.get(Order, id_order)

    def get_order_service(self, id_order: int, id_service: int) -> OrderToService:
        return self.__session.query(OrderToService).where(OrderToService.id_order == id_order).\
            where(OrderToService.id_service == id_service).first()

    def get_by_trace_id(self, uuid: str) -> Order:
        return self.__session.query(Order).where(Order.trace_id == uuid).first()

    def get_order_by_auto_mechanic_id_and_state_order(self, auto_mechanic_id: int, state_order: int) -> list[Order]:
        return self.__session.query(Order).join(StateOrder).\
            where(StateOrder.id == state_order).\
            where(Order.auto_mechanic_id == auto_mechanic_id).all()

    def get_list_order(self) -> list[Order]:
        return self.__session.query(Order).all()

    def get_state_order(self) -> list[Order]:
        return self.__session.query(StateOrder).all()

    def add(self, client_trace_id: str, auto_mechanic_id: int, auto_id: int, state_order_id: int, description: str) -> Order:

        client_entity = self.__session.query(Client).where(Client.trace_id == client_trace_id).first()

        entity = Order(
            client_id=client_entity.id,
            auto_mechanic_id=auto_mechanic_id,
            auto_id=auto_id,
            state_order_id=state_order_id,
            description=description
        )

        try:
            self.__session.add(entity)
            self.__session.commit()
            return entity
        except:
            self.__session.rollback()
            return None

    def update_order_service(self, id_order: int, id_service: int, count: int):
        entity = self.get_order_service(id_order, id_service)
        entity.count = count
        try:
            self.__session.commit()
        except:
            self.__session.rollback()

    def update(self, id_trace: str, auto_mechanic: int, auto: int, state_order: int, description: str):
        entity = self.get_by_trace_id(id_trace)

        entity.auto_mechanic_id = auto_mechanic
        entity.auto_id = auto
        entity.state_order_id = state_order
        entity.description = description

        try:
            self.__session.commit()
        except:
            self.__session.rollback()