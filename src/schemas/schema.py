from typing import Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, PositiveFloat, PositiveInt, field_validator


class ItemSchema(BaseModel):
    produto: str
    unidade_medida: Literal['litro', 'metro', 'quilograma', 'metro_cubico', 'quantidade']
    custo_medio: PositiveFloat = Field(..., ge=0)
    valor_venda: PositiveFloat = Field(..., ge=0)
    estoque: Union[PositiveFloat, PositiveInt] = Field(..., ge=0)

    @field_validator('produto')
    def produto_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Produto não pode ser vazio')
        return v


class ItemCreate(ItemSchema):
    pass


class ItemUpdate(ItemSchema):
    produto: Optional[str]
    unidade_medida: Optional[Literal['litro', 'metro', 'quilograma', 'metro_cubico', 'quantidade']]
    custo_medio: Optional[PositiveFloat] = Field(None, ge=0)
    valor_venda: Optional[PositiveFloat] = Field(None, ge=0)
    estoque: Optional[Union[PositiveFloat, PositiveInt]] = Field(None, ge=0)


class ItemResponse(ItemSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
