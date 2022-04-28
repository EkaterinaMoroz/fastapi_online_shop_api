import bcrypt
from sqlalchemy.orm import Session

import schemas
import src.models as models


# Get user by username function
def get_user_by_username(db: Session, username: str):
    return db.query(models.UserInfo).filter(models.UserInfo.username == username).first()


# User registration function
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = models.UserInfo(username=user.username, password=hashed_password, fullname=user.fullname)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Login Function
def login(db: Session, username: str, password: str):
    db_user = db.query(models.UserInfo).filter(models.UserInfo.username == username).first()
    print(username, password)
    passw = bcrypt.checkpw(password.encode('utf-8'), db_user.password)
    return passw


# Get item by id function
def get_item_by_id(db: Session, id: int):
    return db.query(models.ItemInfo).filter(models.ItemInfo.id == id).first()


# Add items to DB function
def add_table(db: Session, item: schemas.ItemInfo):
    db_item = models.ItemInfo(itemname=item.itemname, itemprice=item.itemprice, itemamount=item.itemamount)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# Delete item from DB by id function
def delete_item_by_id(db: Session, id: int):
    delitem = db.query(models.ItemInfo).filter(models.ItemInfo.id == id).first()
    if delitem is None:
        return
    db.delete(delitem)
    db.commit()
    return delitem


# Add to cart function
def add_to_cart(db: Session, username: str, items: models.CartInfo):
    user = db.query(models.UserInfo).filter(models.UserInfo.username == username).first()
    db_cart = models.CartInfo(ownername=user.id, itemname=items.itemname, itemprice=items.itemprice, )
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart


# Delete item in the cart by id
def delete_cart_item_by_id(db: Session, id: int):
    delitem = db.query(models.CartInfo).filter(models.CartInfo.id == id).first()
    if delitem is None:
        return
    db.delete(delitem)
    db.commit()
    return delitem


def payment(db: Session, phone_number: int, total: int):
    pass
