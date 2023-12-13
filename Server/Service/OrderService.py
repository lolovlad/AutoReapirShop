from ..Repository import OrderRepository, UserRepository, ServiceRepository
from ..database import db, Order, User, StateOrder, Service, OrderToService
from ..Models import OrderViewAdmin
from sqlalchemy.orm import Session


class OrderService:
    def __init__(self, session: Session):
        self.__session: Session = session
        self.__repository_order: OrderRepository = OrderRepository(session)
        self.__repository_user: UserRepository = UserRepository(session)
        self.__repository_service: ServiceRepository = ServiceRepository(session)

    def get_order_service(self, id_order: int, id_service: int) -> OrderToService:
        return self.__repository_order.get_order_service(id_order, id_service)

    def get(self, id_order: int) -> Order:
        return self.__repository_order.get(id_order)

    def get_order_by_auto_mechanic_id_and_state_order(self, auto_mechanic_id: int, state_order: int) -> list[Order]:
        return self.__repository_order.get_order_by_auto_mechanic_id_and_state_order(auto_mechanic_id, state_order)

    def get_by_trace_id(self, uuid: str) -> Order:
        return self.__repository_order.get_by_trace_id(uuid)

    def get_list_order(self) -> list[Order]:
        return self.__repository_order.get_list_order()

    def get_auto_mechanic(self) -> list[User]:
        return self.__repository_user.get_list_by_worker()

    def get_state_order(self) -> list[StateOrder]:
        return self.__session.query(StateOrder).all()

    def get_list_service(self) -> list[Service]:
        return self.__repository_service.get_list_service()

    def add(self, client_trace_id: str, auto_mechanic_id: int,
            auto_id: int, state_order_id: int, description: str,
            service_list_id: list[int]):
        order_entity = self.__repository_order.add(client_trace_id,
                                                   auto_mechanic_id,
                                                   auto_id,
                                                   state_order_id,
                                                   description)
        if order_entity is not None:
            self.__repository_service.add_all(order_entity.id, service_list_id)

    def update_order_service(self, id_order: int, id_service: int, count: int):
        self.__repository_order.update_order_service(id_order, id_service, count)

    def update(self, id_trace: str, auto_mechanic: int, auto: int, state_order: int, description: str):
        self.__repository_order.update(id_trace, auto_mechanic, auto, state_order, description)
