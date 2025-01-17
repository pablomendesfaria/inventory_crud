from typing import List

from controller import crud
from fastapi import APIRouter, Depends, HTTPException
from models.database import get_db
from schemas.schema import ItemCreate, ItemResponse, ItemUpdate, MovementHistoryResponse
from sqlalchemy.orm import Session

router = APIRouter()


@router.get('/items', response_model=List[ItemResponse])
def read_items(db: Session = Depends(get_db)):
    """Get all items.

    Args:
        db (Session): The database session.

    Returns:
        List[ItemResponse]: A list of all items.
    """
    items = crud.get_items(db)
    if not items:
        raise HTTPException(status_code=404, detail='Nenhum item encontrado')
    return items


@router.get('/items/{item_id}', response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    """Get an item by ID.

    Args:
        item_id (int): The item ID.
        db (Session): The database session.

    Returns:
        ItemResponse: The item with the given ID.

    Raises:
        HTTPException: If the item is not found.
    """
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail='Item não encontrado')
    return item


@router.post('/items', response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """Create a new item.

    Args:
        item (ItemCreate): The item data.
        db (Session): The database session.

    Returns:
        ItemResponse: The created item.
    """
    return crud.create_item(db, item)


@router.put('/items/{item_id}', response_model=ItemResponse)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    """Update an existing item.

    Args:
        item_id (int): The item ID.
        item (ItemUpdate): The updated item data.
        db (Session): The database session.

    Returns:
        ItemResponse: The updated item.

    Raises:
        HTTPException: If the item is not found.
    """
    updated_item = crud.update_item(db, item_id, item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail='Item não encontrado')
    return updated_item


@router.delete('/items/{item_id}', response_model=ItemResponse)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete an item by ID.

    Args:
        item_id (int): The item ID.
        db (Session): The database session.

    Returns:
        ItemResponse: The deleted item.

    Raises:
        HTTPException: If the item is not found.
    """
    deleted_item = crud.delete_item(db, item_id)
    if deleted_item is None:
        raise HTTPException(status_code=404, detail='Item não encontrado')
    return deleted_item


@router.get('/movements/{product_id}', response_model=List[MovementHistoryResponse])
def get_product_movement_history(product_id: int, db: Session = Depends(get_db)):
    """Get the movement history for a product.

    Args:
        product_id (int): The product ID.
        db (Session): The database session.

    Returns:
        List[MovementHistoryResponse]: A list of movement history records for the product.

    Raises:
        HTTPException: If no movements are found for the product.
    """
    movements = crud.get_product_movement_history(db, product_id)
    if movements is None:
        raise HTTPException(status_code=404, detail='Nenhum historico de movimento encontrado para este produto')
    return movements
