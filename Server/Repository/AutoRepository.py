from sqlalchemy.orm import Session
from sqlalchemy import func, select
from ..Models import BaseOrder
from ..database import Auto, Client


class AutoRepository:
    def __init__(self, session: Session):
        self.__session: Session = session

    def get(self, id_auto: int) -> Auto:
        return self.__session.get(Auto, id_auto)

    def get_by_trace_id(self, id_trace: str) -> Auto:
        return self.__session.query(Auto).where(Auto.trace_id == id_trace).first()

    def get_list_auto_by_trace(self, id_trace_client: str) -> list[Auto]:
        return self.__session.query(Auto).join(Client).where(Client.trace_id == id_trace_client).all()

    def get_list_auto_by_id(self, id_client: int) -> list[Auto]:
        return self.__session.query(Auto).join(Client).where(Client.id == id_client).all()

    def add(self, id_client: int, model: str, brand: str, number: str, region: str, vin_number: str):
        entity = Auto(
            id_client=id_client,
            model=model,
            brand=brand,
            number=number,
            region=region,
            vin_number=vin_number
        )
        try:
            self.__session.add(entity)
            self.__session.commit()
        except:
            self.__session.rollback()

    def update(self, id_trace: str, model: str, brand: str, number: str, region: str, vin_number: str):
        entity = self.get_by_trace_id(id_trace)

        entity.model = model
        entity.brand = brand
        entity.number = number
        entity.region = region
        entity.vin_number = vin_number

        try:
            self.__session.commit()
        except:
            self.__session.rollback()

    def delete(self, id_auto: str):
        entity = self.get_by_trace_id(id_auto)
        try:
            self.__session.delete(entity)
            self.__session.commit()
        except:
            self.__session.rollback()

