from pydantic import BaseModel


# base schema for user data
class UserInfoBase(BaseModel):
    username: str
    fullname: str
    isSeller: bool


# schema for user registration
class UserCreate(UserInfoBase):
    password: str


# schema for getting user by id
class UserInfo(UserInfoBase):
    id: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str


# base schema for items
class ItemInfo(BaseModel):
    itemname: str
    itemprice: int
    itemamount: int


# used for getting item by id
class ItemAInfo(ItemInfo):
    id: int

    class Config:
        orm_mode = True


# base schema for relating a cart to it's user
class CartOwnerInfo(BaseModel):
    username: str


# base schema for adding items to cart
class CartInfo(BaseModel):
    itemname: str
    itemprice: int
    itemamount: int


# base schema for getting items in the cart by id
class CartItemAInfo(CartInfo):
    id: int

    class Config:
        orm_mode = True


# base schema for the payment api
class UserPayment(BaseModel):
    phonenumber: int
    total: int
