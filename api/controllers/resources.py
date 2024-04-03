from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import models, schemas  # Update the import path if necessary

def create(db: Session, resource: schemas.ResourceCreate):
    db_resource = models.Resource(
        item=resource.item,
        amount=resource.amount
    )
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

def read_all(db: Session):
    return db.query(models.Resource).all()

def read_one(db: Session, resource_id: int):
    resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

def update(db: Session, resource_id: int, resource: schemas.ResourceUpdate):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id)
    if db_resource.first() is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    db_resource.update(resource.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return db_resource.first()

def delete(db: Session, resource_id: int):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id)
    if db_resource.first() is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    db_resource.delete(synchronize_session=False)
    db.commit()
    return {"message": "Resource deleted successfully"}