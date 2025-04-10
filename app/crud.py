from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime, timedelta


def get_table(db: Session, table_id: int):
    return db.query(models.Table).filter(models.Table.id == table_id).first()


def get_tables(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Table).offset(skip).limit(limit).all()


def create_table(db: Session, table: schemas.TableCreate):
    db_table = models.Table(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table


def delete_table(db: Session, table_id: int):
    db_table = db.query(models.Table).filter(models.Table.id == table_id).first()
    if db_table:
        db.delete(db_table)
        db.commit()
        return True
    return False


def get_reservation(db: Session, reservation_id: int):
    return db.query(models.Reservation).filter(
        models.Reservation.id == reservation_id).first()


def get_reservations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Reservation).offset(skip).limit(limit).all()


def create_reservation(db: Session, reservation: schemas.ReservationCreate):
    # Check if table exists
    table = get_table(db, reservation.table_id)
    if not table:
        raise ValueError('Table not found')

    # Calculate time range for the reservation
    start_time = reservation.reservation_time
    end_time = start_time + timedelta(minutes=reservation.duration_minutes)

    # Check for overlapping reservations
    overlapping = db.query(models.Reservation).filter(
        models.Reservation.table_id == reservation.table_id,
        models.Reservation.reservation_time < end_time,
        models.Reservation.reservation_time +
        (models.Reservation.duration_minutes * timedelta(minutes=1)) > start_time
    ).first()

    if overlapping:
        raise ValueError('Table is already booked for this time slot')

    db_reservation = models.Reservation(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation


def delete_reservation(db: Session, reservation_id: int):
    db_reservation = db.query(models.Reservation).filter(
        models.Reservation.id == reservation_id).first()
    if db_reservation:
        db.delete(db_reservation)
        db.commit()
        return True
    return False
