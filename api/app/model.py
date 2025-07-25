from pydantic import BaseModel, Field
from typing import Optional, Literal

class ConvertModel(BaseModel): 
    idr: int = 0
    suffix: Optional[Literal['ribu', 'juta']] = None
