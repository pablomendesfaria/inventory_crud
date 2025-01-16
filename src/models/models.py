from sqlalchemy import CheckConstraint, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.models.database import Base


class UoMType(Enum):
    """Enumeration for unit of measure types."""
    LITRO = 'litro'
    METRO = 'metro'
    QUILOGRAMA = 'quilograma'
    METRO_CUBICO = 'metro_cubico'
    QUANTIDADE = 'quantidade'


class MovementType(Enum):
    """Enumeration for movement types."""
    ENTRADA = 'entrada'
    SAIDA = 'saida'


class Item(Base):
    """Model for items.

    Attributes:
        id (int): The item ID.
        produto (str): The product name.
        unidade_medida (Enum): The unit of measure.
        custo_medio (int): The average cost.
        valor_venda (int): The sale value.
        estoque (int): The stock quantity.
    """
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    produto = Column(String, index=True, nullable=False)
    unidade_medida = Column(Enum(UoMType), nullable=False)
    custo_medio = Column(
        Integer,
        CheckConstraint('custo_medio >= 0', name='average_cost_positive'),
    )
    valor_venda = Column(
        Integer,
        CheckConstraint('valor_venda >= 0', name='sale_value_positive'),
    )
    estoque = Column(Integer, CheckConstraint('estoque >= 0', name='stock_positive'), nullable=False)

    def to_dict(self):
        """Convert the item to a dictionary.

        Returns:
            dict: The item as a dictionary.
        """
        return {
            'id': self.id,
            'produto': self.produto,
            'unidade_medida': self.unidade_medida.value,
            'custo_medio': self.custo_medio,
            'valor_venda': self.valor_venda,
            'estoque': self.estoque,
        }


class StockMovementHistory(Base):
    """Model for stock movement history.

    Attributes:
        id (int): The movement ID.
        data (DateTime): The date of the movement.
        movimentacao (Enum): The type of movement.
        id_produto (int): The product ID.
        quantidade (int): The quantity moved.
        estoque_final (int): The final stock quantity.
        produto (relationship): The related product.
    """
    __tablename__ = 'stock_movements_history'

    id = Column(Integer, primary_key=True, index=True)
    data = Column(DateTime(timezone=True), nullable=False)
    movimentacao = Column(Enum(MovementType), nullable=False)
    id_produto = Column(Integer, ForeignKey('items.id'), nullable=False)
    quantidade = Column(Integer, CheckConstraint('quantidade >= 0', name='quantity_positive'), nullable=False)
    estoque_final = Column(
        Integer,
        CheckConstraint('estoque_final >= 0', name='final_stock_positive'),
        nullable=False,
    )

    produto = relationship('Item')

    def to_dict(self):
        """Convert the stock movement history to a dictionary.

        Returns:
            dict: The stock movement history as a dictionary.
        """
        return {
            'id': self.id,
            'data': self.data,
            'movimentacao': self.movimentacao.value,
            'id_produto': self.id_produto,
            'quantidade': self.quantidade,
            'estoque_final': self.estoque_final,
        }
