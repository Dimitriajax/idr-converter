from pydantic import BaseModel

class TransferModel(BaseModel): 
    send_amount: int
    sender: str
    receiver: str

