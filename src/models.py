from sqlalchemy import Column, Integer, String, Boolean

from database import Base


class UserInfo(Base):
    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    fullname = Column(String, unique=True)
    isseller = Column(Boolean)


class ItemInfo(Base):
    __tablename__ = "item_info"

    id = Column(Integer, primary_key=True, index=True)
    itemname = Column(String, unique=True)
    itemprice = Column(Integer)
    itemamount = Column(Integer)


class CartInfo(Base):
    __tablename__ = "cart_info"

    id = Column(Integer, primary_key=True, index=True)
    ownername = Column(Integer, unique=True)
    itemname = Column(String, unique=True)
    itemprice = Column(Integer)
