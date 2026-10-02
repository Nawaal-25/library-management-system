from datetime import date
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import Book, Member, Transaction
from schemas import (
    BookCreate,
    BookResponse,
    MemberCreate,
    MemberResponse,
    TransactionCreate,
    TransactionResponse
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Online Library Management System")


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/books", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    existing_book = db.query(Book).filter(Book.isbn == book.isbn).first()

    if existing_book:
        raise HTTPException(status_code=400, detail="ISBN already exists")

    new_book = Book(
        title=book.title,
        author=book.author,
        isbn=book.isbn,
        quantity=book.quantity,
        available_quantity=book.quantity
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


@app.get("/books", response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()
@app.post("/members", response_model=MemberResponse)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    existing_member = db.query(Member).filter(Member.email == member.email).first()

    if existing_member:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_member = Member(
        name=member.name,
        email=member.email,
        phone=member.phone,
        membership_date=member.membership_date
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return new_member


@app.get("/members", response_model=list[MemberResponse])
def get_members(db: Session = Depends(get_db)):
    return db.query(Member).all()


@app.post("/transactions/issue", response_model=TransactionResponse)
def issue_book(transaction: TransactionCreate, db: Session = Depends(get_db)):

    book = db.query(Book).filter(Book.id == transaction.book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    member = db.query(Member).filter(Member.id == transaction.member_id).first()

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    if book.available_quantity <= 0:
        raise HTTPException(status_code=400, detail="Book is not available")

    new_transaction = Transaction(
        book_id=transaction.book_id,
        member_id=transaction.member_id,
        issue_date=date.today(),
        status="Issued"
    )

    book.available_quantity -= 1

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction

@app.post("/transactions/{transaction_id}/return")
def return_book(transaction_id: int, db: Session = Depends(get_db)):

    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    if transaction.status == "Returned":
        raise HTTPException(status_code=400, detail="Book already returned")

    book = db.query(Book).filter(Book.id == transaction.book_id).first()

    transaction.return_date = date.today()
    transaction.status = "Returned"

    book.available_quantity += 1

    db.commit()

    return {
        "message": "Book returned successfully",
        "transaction_id": transaction.id
    }
@app.get("/transactions")
def get_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()