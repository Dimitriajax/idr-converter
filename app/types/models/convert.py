from pydantic import BaseModel, Field
from typing import Optional, Literal
from dataclasses import dataclass

class ConvertModel(BaseModel): 
    idr: int = Field(..., gt=0)
    suffix: Optional[Literal['ribu', 'juta']] = None