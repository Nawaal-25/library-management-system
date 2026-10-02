from datetime import date
from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    quantity: int = 1


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    quantity: int
    available_quantity: int

    class Config:
        from_attributes = True

class MemberCreate(BaseModel):
    name: str
    email: str
    phone: str
    membership_date: str


class MemberResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    membership_date: date

    class Config:
        from_attributes = True

class TransactionCreate(BaseModel):
    book_id: int
    member_id: int


class TransactionResponse(BaseModel):
    id: int
    book_id: int
    member_id: int
    issue_date: date
    return_date: str | None
    status: str

    class Config:
        from_attributes = True