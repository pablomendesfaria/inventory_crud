from datetime import datetime

from sqlalchemy import CheckConstraint, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.models.database import Base


class UoMType(Enum):
    LITRO = 'litro'
    METRO = 'metro'
    QUILOGRAMA = 'quilograma'
    METRO_CUBICO = 'metro_cubico'
    QUANTIDADE = 'quantidade'


class MovementType(Enum):
    ENTRADA = 'entrada'
    SAIDA = 'saida'


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    produto = Column(String, index=True)
    unidade_medida = Column(Enum(UoMType), nullable=False)
    custo_medio = Column(
        Integer,
        CheckConstraint('custo_medio >= 0', name='average_cost_positive'),
    )
    valor_venda = Column(
        Integer,
        CheckConstraint('valor_venda >= 0', name='sale_value_positive'),
    )
    estoque = Column(Integer, CheckConstraint('estoque >= 0', name='stock_positive'))

    def to_dict(self):
        return {
            'id': self.id,
            'produto': self.produto,
            'unidade_medida': self.unidade_medida.value,
            'custo_medio': self.custo_medio,
            'valor_venda': self.valor_venda,
            'estoque': self.estoque,
        }


class StockMovement(Base):
    __tablename__ = 'stock_movements'

    id = Column(Integer, primary_key=True, index=True)
    data = Column(DateTime, default=datetime.now(datetime.timezone.utc), nullable=False)
    movimentacao = Column(Enum(MovementType), nullable=False)
    id_produto = Column(Integer, ForeignKey('items.id'), nullable=False)
    quantidade = Column(Integer, CheckConstraint('quantidade >= 0', name='quantity_positive'))
    estoque_final = Column(
        Integer,
        CheckConstraint('estoque_final >= 0', name='final_stock_positive'),
    )

    produto = relationship('Item')

    def to_dict(self):
        return {
            'id': self.id,
            'data': self.data.isoformat(),
            'movimentacao': self.movimentacao.value,
            'id_produto': self.id_produto,
            'quantidade': self.quantidade,
            'estoque_final': self.estoque_final,
        }
