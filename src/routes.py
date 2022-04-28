import uvicorn
from fastapi import Depends
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
import src.models as models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/register", response_model=schemas.UserInfo)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@app.post("/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.login(db, username=user.username, password=user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Wrong username/password")
    return {"message": "User found"}


@app.get("/get_user/{username}", response_model=schemas.UserInfo)
def get_user(username, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=username)
    return db_user


# add items to DB API
@app.post("/add_item", response_model=schemas.ItemInfo)
def add_item(user: schemas.UserInfoBase, item: schemas.ItemInfo, db: Session = Depends(get_db), ):
    if user.isSeller:
        db_item = crud.add_table(db=db, item=item)
        if db_item:
            raise HTTPException(status_code=200, detail="item registered")
    else:
        raise HTTPException(status_code=403, detail="not allowed")


# get item by id API
@app.get("/get_item/{id}", response_model=schemas.ItemAInfo)
def get_item(id, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_id(db, id=id)
    if db_item is None:
        raise HTTPException(status_code=400, detail="No item found")
    elif db_item.itemamount < 1:
        raise HTTPException(status_code=404, detail="No item found")
    return db_item


# delete item by id API
@app.delete("/del_item/{id}", response_model=schemas.ItemAInfo)
def del_user(id, db: Session = Depends(get_db)):
    db_item = crud.delete_item_by_id(db, id=id)
    if db_item:
        raise HTTPException(status_code=200, detail="Item found to delete")
    else:
        raise HTTPException(status_code=400, detail="Item Not found to delete")


# add to cart by username and the items to be added API
@app.post("/add_to_cart/{username}", response_model=schemas.CartOwnerInfo)
def add_to_cart(username, item: schemas.ItemInfo, items: schemas.CartInfo, db: Session = Depends(get_db)):
    if item.itemamount > 0:
        db_cart = crud.add_to_cart(db=db, username=username, items=items)
        if db_cart:
            raise HTTPException(status_code=200, detail="item registered to cart")
    else:
        raise HTTPException(status_code=404, detail="no item left")


# delete items in the cart by id API
@app.delete("/del_cart_item/{id}", response_model=schemas.CartItemAInfo)
def del_user(id, db: Session = Depends(get_db)):
    db_item = crud.delete_cart_item_by_id(db, id=id)
    if db_item:
        raise HTTPException(status_code=200, detail="Item found to delete")
    else:
        raise HTTPException(status_code=400, detail="Item Not found to delete")


# payment API
@app.post("/payment")
def add_item(userphone: schemas.UserPayment, db: Session = Depends(get_db)):
    user_payment = crud.payment(db=db, phone_number=userphone.phonenumber, total=userphone.total)
    if user_payment:
        raise HTTPException(status_code=200, detail="payment Started")
    return


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8081)
