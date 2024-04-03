from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import models, schemas  # Update the import path if necessary

def create(db: Session, recipe: schemas.RecipeCreate):
    db_recipe = models.Recipe(
        sandwich_id=recipe.sandwich_id,
        resource_id=recipe.resource_id,
        amount=recipe.amount
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def read_all(db: Session):
    return db.query(models.Recipe).all()

def read_one(db: Session, recipe_id: int):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

def update(db: Session, recipe_id: int, recipe: schemas.RecipeUpdate):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id)
    if db_recipe.first() is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db_recipe.update(recipe.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return db_recipe.first()

def delete(db: Session, recipe_id: int):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id)
    if db_recipe.first() is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db_recipe.delete(synchronize_session=False)
    db.commit()
    return {"message": "Recipe deleted successfully"}