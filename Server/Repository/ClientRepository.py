from sqlalchemy.orm import Session
from sqlalchemy import func, select
from ..Models import BaseOrder
from ..database import Client


class ClientRepository:
    def __init__(self, session: Session):
        self.__session: Session = session

    def get(self, id_client: int) -> Client:
        return self.__session.get(Client, id_client)

    def get_by_trace_id(self, id_trace: str) -> Client:
        return self.__session.query(Client).where(Client.trace_id == id_trace).first()

    def get_list_client(self) -> list[Client]:
        return self.__session.query(Client).all()

    def add(self, name: str, surname: str, patronymics: str, phone: str, email: str):
        entity = Client(
            name=name,
            surname=surname,
            patronymics=patronymics,
            phone=phone,
            email=email
        )
        try:
            self.__session.add(entity)
            self.__session.commit()
        except:
            self.__session.rollback()

    def update(self, id_trace: str, name: str, surname: str, patronymics: str, phone: str, email: str):
        entity = self.get_by_trace_id(id_trace)

        entity.name = name
        entity.surname = surname
        entity.patronymics = patronymics
        entity.phone = phone
        entity.email = email

        try:
            self.__session.commit()
        except:
            self.__session.rollback()

    def delete(self, id_client: str):
        entity = self.get_by_trace_id(id_client)
        try:
            self.__session.delete(entity)
            self.__session.commit()
        except:
            self.__session.rollback()

