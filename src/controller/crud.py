from sqlalchemy.orm import Session

from src.models.models import Item, StockMovement
from src.schemas.schema import ItemCreate, ItemUpdate, MovementSchema


def get_items(db: Session):
    return db.query(Item).all()


def get_item(db: Session, item_id: int):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        return None
    return item


def create_item(db: Session, item: ItemCreate):
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
    return new_item


def update_item(db: Session, item_id: int, item_update: ItemUpdate):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        return None

    for key, value in item_update.dict(exclude_unset=True).items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return item


def delete_item(db: Session, item_id: int):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        return None

    db.delete(item)
    db.commit()
    return item


def get_movement(db: Session, product_id: int):
    movement = db.query(StockMovement).filter(StockMovement.id_produto == product_id).first()
    if movement is None:
        return None
    return movement


def create_movement(db: Session, movement: MovementSchema):
    if movement.tipo_movimentacao == 'entrada':
        item.estoque += movement.quantidade
    elif movement.tipo_movimentacao == 'saida':
        item.estoque -= movement.quantidade

    new_movement = StockMovement(
        data_movimentacao=movement.data_movimentacao,
        tipo_movimentacao=movement.tipo_movimentacao,
        produto_id=movement.produto_id,
        quantidade=movement.quantidade,
        estoque_final=item.estoque,
    )

    db.add(new_movement)
    db.commit()
    db.refresh(new_movement)
    return new_movement
