import datetime
import enum
from uuid import uuid4

from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Enum, Float, Text, MetaData
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

'''
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}'''

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)


class Role(db.Model):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

    def __repr__(self):
        return f"{self.name}"


class Type(db.Model):
    __tablename__ = "type"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String(255))

    def __repr__(self):
        return f"{self.name}"


class StateOrder(db.Model):
    __tablename__ = "state_order"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String(255))

    def __repr__(self):
        return f"{self.name}"


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trace_id = Column(String, unique=True, default=str(uuid4()))
    name = Column(String(32), nullable=False)
    surname = Column(String(32), nullable=False)
    patronymics = Column(String(32), nullable=False)

    phone = Column(String(20), nullable=False)
    email = Column(String(32), nullable=False)

    role_id = Column(Integer, ForeignKey('role.id'))
    role = relationship("Role")

    password_hash = Column(String, nullable=False)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, val):
        self.password_hash = generate_password_hash(val, "sha256")

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"{self.surname} {self.name[0]}. {self.patronymics[0]}."


class Client(db.Model):
    __tablename__ = "client"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trace_id = Column(String, unique=True, default=str(uuid4()))
    name = Column(String(32), nullable=False)
    surname = Column(String(32), nullable=False)
    patronymics = Column(String(32), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(32), nullable=False)

    auto = relationship("Auto", back_populates="client")

    def __repr__(self):
        return f"{self.surname} {self.name[0]}. {self.patronymics[0]}."


class Order(db.Model):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trace_id = Column(String, unique=True, default=str(uuid4()))

    client_id = Column(Integer, ForeignKey('client.id'))
    client = relationship("Client")

    auto_mechanic_id = Column(Integer, ForeignKey('user.id'))
    auto_mechanic = relationship("User")

    auto_id = Column(Integer, ForeignKey('auto.id'))
    auto = relationship("Auto")

    state_order_id = Column(Integer, ForeignKey('state_order.id'))
    state_order = relationship("StateOrder")

    datatime_order = Column(DateTime, nullable=False, default=datetime.datetime.now())
    description = Column(Text, nullable=True)
    services = relationship("OrderToService")


class Service(db.Model):
    __tablename__ = "service"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trace_id = Column(String, unique=True, default=str(uuid4()))
    name = Column(String(126), nullable=False)

    type_id = Column(Integer, ForeignKey('type.id'), nullable=True)
    type = relationship("Type")

    price = Column(Float, nullable=False, default=0.00)

    def __repr__(self):
        return f"{self.name}"


class OrderToService(db.Model):
    __tablename__ = "order_to_service"
    id_order = Column(ForeignKey("order.id"), primary_key=True)
    id_service = Column(ForeignKey("service.id"), primary_key=True)
    service = relationship("Service")
    price = Column(Float, nullable=False)
    count = Column(Integer, nullable=False, default=1)

    def __repr__(self):
        return f"{self.service.name} {self.price}"


class Auto(db.Model):
    __tablename__ = "auto"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trace_id = Column(String, unique=True, default=str(uuid4()))

    id_client = Column(ForeignKey("client.id"))
    client = relationship("Client", back_populates="auto")

    model = Column(String(32), nullable=False)
    brand = Column(String(32), nullable=False)
    number = Column(String(6), nullable=False)
    region = Column(String(3), nullable=False)
    vin_number = Column(String, nullable=False)

    def __repr__(self):
        return f"{self.model} {self.brand}"


#######################################################################


'''class Bakery(db.Model):
    __tablename__ = "bakery"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trace_id = Column(String, unique=True, default=str(uuid4()))

    name = Column(String(32), nullable=False)
    address = Column(String, nullable=False)
    description = Column(Text, nullable=True)'''