from ..Repository import ClientRepository
from sqlalchemy.orm import Session
from ..database import Client


class ClientService:
    def __init__(self, session: Session):
        self.__repository: ClientRepository = ClientRepository(session)

    def get(self, id_client: int) -> Client:
        return self.__repository.get(id_client)

    def get_by_trace_id(self, id_trace: str) -> Client:
        return self.__repository.get_by_trace_id(id_trace)

    def get_list_client(self) -> list[Client]:
        return self.__repository.get_list_client()

    def add(self, name: str, surname: str, patronymics: str, phone: str, email: str):
        self.__repository.add(name, surname, patronymics, phone, email)

    def update(self, id_client: str, name: str, surname: str, patronymics: str, phone: str, email: str):
        self.__repository.update(id_client, name, surname, patronymics, phone, email)

    def delete(self, id_client: str):
        self.__repository.delete(id_client)
