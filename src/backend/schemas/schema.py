from datetime import datetime
from typing import Optional, Union

from models.models import MovementType, UoMType
from pydantic import BaseModel, ConfigDict, Field, PositiveFloat, PositiveInt, field_validator


class ItemSchema(BaseModel):
    """Schema for item data.

    Attributes:
        produto (str): The product name.
        unidade_medida (Literal): The unit of measure.
        custo_medio (PositiveFloat): The average cost.
        valor_venda (PositiveFloat): The sale value.
        estoque (PositiveFloat): The stock quantity.
    """

    produto: str
    unidade_medida: UoMType
    custo_medio: PositiveFloat = Field(..., ge=0)
    valor_venda: PositiveFloat = Field(..., ge=0)
    estoque: PositiveFloat = Field(..., ge=0)

    @field_validator('produto')
    def produto_must_not_be_empty(cls, v):
        """Validate that the product name is not empty.

        Args:
            v (str): The product name.

        Returns:
            str: The validated product name.

        Raises:
            ValueError: If the product name is empty.
        """
        if not v.strip():
            raise ValueError('Produto não pode ser vazio')
        return v


class ItemCreate(ItemSchema):
    """Schema for creating an item."""

    pass


class ItemUpdate(ItemSchema):
    """Schema for updating an item.

    Attributes:
        produto (Optional[str]): The product name.
        unidade_medida (Optional[Literal]): The unit of measure.
        custo_medio (Optional[PositiveFloat]): The average cost.
        valor_venda (Optional[PositiveFloat]): The sale value.
        estoque (Optional[PositiveFloat]): The stock quantity.
    """

    produto: Optional[str]
    unidade_medida: Optional[UoMType]
    custo_medio: Optional[PositiveFloat] = Field(None, ge=0)
    valor_venda: Optional[PositiveFloat] = Field(None, ge=0)
    estoque: Optional[PositiveFloat] = Field(None, ge=0)


class ItemResponse(ItemSchema):
    """Schema for item response.

    Attributes:
        id (int): The item ID.
    """

    model_config = ConfigDict(from_attributes=True)
    id: int


class MovementHistorySchema(BaseModel):
    """Schema for movement data.

    Attributes:
        data (datetime): The movement date.
        movimentacao (Literal): The movement type.
        produto_id (int): The item ID.
        quantidade (PositiveFloat): The quantity.
        estoque_final (PositiveFloat): The final stock quantity.
    """

    data: datetime
    movimentacao: MovementType
    produto_id: int
    quantidade: PositiveFloat = Field(..., ge=0)
    estoque_final: PositiveFloat = Field(..., ge=0)


class MovementHistoryResponse(MovementHistorySchema):
    """Schema for movement response.

    Attributes:
        id (int): The movement ID.
    """

    model_config = ConfigDict(from_attributes=True)
    id: int
