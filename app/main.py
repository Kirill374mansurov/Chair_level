from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import SessionLocal, engine
from .exceptions import ReservationConflict, NotFound


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/tables/', response_model=schemas.Table)
def create_table(table: schemas.TableCreate, db: Session = Depends(get_db)):
    return crud.create_table(db=db, table=table)


@app.get('/tables/', response_model=List[schemas.Table])
def read_tables(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tables = crud.get_tables(db, skip=skip, limit=limit)
    return tables


@app.delete('/tables/{table_id}')
def delete_table(table_id: int, db: Session = Depends(get_db)):
    if not crud.delete_table(db=db, table_id=table_id):
        raise NotFound(detail='Table not found')
    return {'ok': True}


@app.post('/reservations/', response_model=schemas.Reservation)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_reservation(db=db, reservation=reservation)
    except ValueError as e:
        if str(e) == 'Table not found':
            raise NotFound(detail=str(e))
        raise ReservationConflict(detail=str(e))


@app.get('/reservations/', response_model=List[schemas.Reservation])
def read_reservations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reservations = crud.get_reservations(db, skip=skip, limit=limit)
    return reservations


@app.delete('/reservations/{reservation_id}')
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    if not crud.delete_reservation(db=db, reservation_id=reservation_id):
        raise NotFound(detail='Reservation not found')
    return {'ok': True}
