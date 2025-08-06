from pydantic import BaseModel

class ConvertedCurrencies(BaseModel):
    eur: float
    usd: float

class ConvertResponse(BaseModel):
    currency: str
    amount: int
    writting: str
    convert: ConvertedCurrencies

class ReverseConvertResponse(BaseModel):
    amount: int
    convert: ConvertedCurrencies