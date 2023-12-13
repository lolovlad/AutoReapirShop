from sqlalchemy.orm import Session
from sqlalchemy import func, select
from ..database import Service, OrderToService


class ServiceRepository:
    def __init__(self, session: Session):
        self.__session: Session = session

    def get(self, id_service: int) -> Service:
        return self.__session.get(Service, id_service)

    def get_list_service(self) -> list[Service]:
        return self.__session.query(Service).all()

    def add_all(self, id_order: int, service_list_id: list[int]):
        services = []

        for i in service_list_id:

            m = self.get(i)

            entity = OrderToService(
                id_order=id_order,
                id_service=i,
                price=m.price,
            )
            services.append(entity)

        try:
            self.__session.add_all(services)
            self.__session.commit()
        except:
            self.__session.rollback()
