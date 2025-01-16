from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.models.models import Item, MovementType, StockMovementHistory
from src.schemas.schema import ItemCreate, ItemUpdate


def get_current_date_formatted(db: Session):
    """Get the current date formatted as DD/MM/YYYY.

    Args:
        db (Session): The database session.

    Returns:
        str: The current date formatted as DD/MM/YYYY.
    """
    result = db.execute(select([func.to_char(func.current_date(), 'DD/MM/YYYY')])).scalar()
    return result


def get_items(db: Session):
    """Get all items.

    Args:
        db (Session): The database session.

    Returns:
        list: A list of all items.
    """
    return db.scalars(select(Item)).all()


def get_item(db: Session, item_id: int):
    """Get an item by ID.

    Args:
        db (Session): The database session.
        item_id (int): The item ID.

    Returns:
        Item: The item with the given ID, or None if not found.
    """
    item = db.get(Item, item_id)
    if item is None:
        return None
    return item


def create_item(db: Session, item: ItemCreate):
    """Create a new item.

    Args:
        db (Session): The database session.
        item (ItemCreate): The item data.

    Returns:
        Item: The created item.
    """
    new_item = Item(
        produto=item.produto,
        unidade_medida=item.unidade_medida,
        custo_medio=item.custo_medio,
        valor_venda=item.valor_venda,
        estoque=item.estoque,
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    # Criar histórico de movimentação de entrada
    new_movement = create_movement_history(db, new_item, MovementType.ENTRADA, new_item.estoque)
    db.add(new_movement)
    db.commit()
    db.refresh(new_movement)
    return new_item


def update_item(db: Session, item_id: int, item_update: ItemUpdate):
    """Update an existing item.

    Args:
        db (Session): The database session.
        item_id (int): The item ID.
        item_update (ItemUpdate): The updated item data.

    Returns:
        Item: The updated item, or None if not found.
    """
    item = db.get(Item, item_id)
    if item is None:
        return None

    # Armazenar o estoque antes da atualização
    estoque_anterior = item.estoque

    for key, value in item_update.model_dump(exclude_unset=True).items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)

    # Determinar o tipo de movimentação com base na diferença de estoque
    if item.estoque > estoque_anterior:
        tipo_movimentacao = MovementType.ENTRADA
        quantidade = item.estoque - estoque_anterior
    elif item.estoque < estoque_anterior:
        tipo_movimentacao = MovementType.SAIDA
        quantidade = estoque_anterior - item.estoque
    else:
        # Se o estoque não mudou, não criar movimentação
        return item

    # Criar histórico de movimentação
    new_movement = create_movement_history(db, item, tipo_movimentacao, quantidade)
    db.add(new_movement)
    db.commit()
    db.refresh(new_movement)

    return item


def delete_item(db: Session, item_id: int):
    """Delete an item by ID.

    Args:
        db (Session): The database session.
        item_id (int): The item ID.

    Returns:
        Item: The deleted item, or None if not found.
    """
    item = db.get(Item, item_id)
    if item is None:
        return None

    db.delete(item)
    db.commit()
    return item


def get_product_movement_history(db: Session, product_id: int):
    """Get the movement history for a product.

    Args:
        db (Session): The database session.
        product_id (int): The product ID.

    Returns:
        list: A list of movement history records for the product.
    """
    movements = db.scalars(select(StockMovementHistory).filter_by(id_product=product_id)).all()
    if movements is None:
        return None
    return movements


def create_movement_history(db: Session, item: Item, tipo_movimentacao: MovementType, quantidade: int):
    """Create a new stock movement history record.

    Args:
        db (Session): The database session.
        item (Item): The item.
        tipo_movimentacao (MovementType): The type of movement.
        quantidade (int): The quantity moved.

    Returns:
        StockMovementHistory: The created stock movement history record.
    """
    new_movement = StockMovementHistory(
        data_movimentacao=get_current_date_formatted(db),
        tipo_movimentacao=tipo_movimentacao,
        produto_id=item.id,
        quantidade=quantidade,
        estoque_final=item.estoque,
    )
    return new_movement
