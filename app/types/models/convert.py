from pydantic import BaseModel, Field, validator
from typing import Optional, Literal

class ConvertModel(BaseModel): 
    idr: int
    suffix: Optional[Literal['ribu', 'juta']] = None