from ..Repository import AutoRepository, ClientRepository
from sqlalchemy.orm import Session
from ..database import Auto


class AutoService:
    def __init__(self, session: Session):
        self.__repository: AutoRepository = AutoRepository(session)
        self.__client_repo: ClientRepository = ClientRepository(session)

    def get(self, id_client: int) -> Auto:
        return self.__repository.get(id_client)

    def get_by_trace_id(self, id_trace: str) -> Auto:
        return self.__repository.get_by_trace_id(id_trace)

    def get_list_auto_by_trace(self, id_client_trace: str) -> list[Auto]:
        return self.__repository.get_list_auto_by_trace(id_client_trace)

    def get_list_auto_by_id(self, id_client: int) -> list[Auto]:
        return self.__repository.get_list_auto_by_id(id_client)

    def add(self, id_trace: str, model: str, brand: str, number: str, region: str, vin_number: str):
        client = self.__client_repo.get_by_trace_id(id_trace)
        self.__repository.add(client.id, model, brand, number, region, vin_number)

    def update(self, id_trace: str, model: str, brand: str, number: str, region: str, vin_number: str):
        self.__repository.update(id_trace, model, brand, number, region, vin_number)

    def delete(self, id_auto: str):
        self.__repository.delete(id_auto)
